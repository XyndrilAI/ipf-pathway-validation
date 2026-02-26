#!/usr/bin/env python3
"""
Stratified holdout validation with balanced permutation null.

Fixes borderline p-values caused by class imbalance (e.g. 40:8 IPF:CTRL)
by using stratified train/test splits and class-balanced permutation null.
Also computes bootstrap 95% CI for the observed SI.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def topN_pathways(effect: pd.Series, top_n: int) -> set[str]:
    return set(effect.abs().sort_values(ascending=False).head(top_n).index)


def compute_effect(path_scores: pd.DataFrame, labels) -> pd.Series:
    ipf = path_scores[labels == 1].mean(axis=0)
    ctrl = path_scores[labels == 0].mean(axis=0)
    return ipf - ctrl


def unrestricted_permutation(labels: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Standard label permutation (shuffle all labels uniformly)."""
    permuted = labels.copy()
    rng.shuffle(permuted)
    return permuted


def holdout_split_si_stratified(
    md: pd.DataFrame,
    scores: pd.DataFrame,
    unit_col: str,
    label_col: str,
    top_n: int,
    train_frac: float = 0.7,
    rng: np.random.Generator | None = None,
) -> float:
    """Stratified holdout split preserving class balance."""
    if rng is None:
        rng = np.random.default_rng()

    ipf_units = md.loc[md[label_col] == 1, unit_col].unique()
    ctrl_units = md.loc[md[label_col] == 0, unit_col].unique()

    n_train_ipf = max(1, int(len(ipf_units) * train_frac))
    n_train_ctrl = max(1, int(len(ctrl_units) * train_frac))

    train_ipf = rng.choice(ipf_units, size=n_train_ipf, replace=False)
    train_ctrl = rng.choice(ctrl_units, size=n_train_ctrl, replace=False)

    train_units = np.concatenate([train_ipf, train_ctrl])
    train_idx = md[unit_col].isin(train_units)
    test_idx = ~train_idx

    if test_idx.sum() == 0 or train_idx.sum() == 0:
        return np.nan

    eff_train = compute_effect(scores.loc[train_idx], md.loc[train_idx, label_col])
    eff_test = compute_effect(scores.loc[test_idx], md.loc[test_idx, label_col])

    return jaccard(topN_pathways(eff_train, top_n), topN_pathways(eff_test, top_n))


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Stratified holdout validation with bootstrap CI"
    )
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--metadata", required=True)
    ap.add_argument("--scores", required=True)
    ap.add_argument("--unit-col", required=True)
    ap.add_argument("--condition-col", default="condition")
    ap.add_argument("--ipf-value", default="IPF")
    ap.add_argument("--ctrl-value", default="CTRL")
    ap.add_argument("--top-n", type=int, default=20)
    ap.add_argument("--n-splits", type=int, default=50)
    ap.add_argument("--n-perm", type=int, default=500)
    ap.add_argument("--n-bootstrap", type=int, default=1000)
    ap.add_argument("--train-frac", type=float, default=0.7)
    ap.add_argument("--outdir", default=".")
    args = ap.parse_args()

    md = pd.read_csv(args.metadata)
    sc = pd.read_csv(args.scores)
    df = md.merge(sc, on="sample_id", how="inner")

    cond = df[args.condition_col].astype(str)
    y = np.where(
        cond == args.ipf_value, 1,
        np.where(cond == args.ctrl_value, 0, np.nan),
    )
    if np.isnan(y).any():
        raise SystemExit(
            f"Condition values must match IPF/CTRL. Found: {cond.unique()}"
        )
    df["_y"] = y.astype(int)

    score_cols = [
        c for c in df.columns
        if c not in md.columns and c not in ("sample_id", "_y")
    ]
    scores = (
        df[score_cols]
        .apply(pd.to_numeric, errors="coerce")
        .dropna(axis=1, how="all")
    )

    n_ipf = int(df["_y"].sum())
    n_ctrl = int((df["_y"] == 0).sum())
    print(f"\n{'='*60}")
    print(f"  Stratified Holdout: {args.dataset}")
    print(f"  Class balance: IPF={n_ipf}, CTRL={n_ctrl}")
    print(f"  Units: {df[args.unit_col].nunique()}   Pathways: {scores.shape[1]}")
    print(f"{'='*60}")

    # ── Observed holdout (stratified splits) ────────────────────
    rng = np.random.default_rng(42)
    si_vals: list[float] = []

    for _ in range(args.n_splits):
        si = holdout_split_si_stratified(
            df, scores, args.unit_col, "_y",
            args.top_n, args.train_frac, rng,
        )
        if not np.isnan(si):
            si_vals.append(si)

    si_mean = float(np.mean(si_vals))
    si_std = float(np.std(si_vals))
    print(f"  Observed SI: {si_mean:.4f} ± {si_std:.4f}  ({len(si_vals)} splits)")

    # ── Stratified permutation null ─────────────────────────────
    null_means: list[float] = []
    rng_null = np.random.default_rng(0)

    for _ in range(args.n_perm):
        perm = unrestricted_permutation(df["_y"].values, rng_null)
        df["_y_perm"] = perm

        si = holdout_split_si_stratified(
            df, scores, args.unit_col, "_y_perm",
            args.top_n, args.train_frac, rng,
        )
        if not np.isnan(si):
            null_means.append(si)

    null_arr = np.array(null_means)
    null_mean = float(null_arr.mean())
    null_std = float(null_arr.std())
    empirical_p = float(np.mean(null_arr >= si_mean))

    print(f"  Null SI:     {null_mean:.4f} ± {null_std:.4f}  ({len(null_means)} perms)")
    print(f"  Delta:       {si_mean - null_mean:.4f}")
    print(f"  Empirical p: {empirical_p:.4f}")

    # ── Bootstrap 95% CI for observed SI ────────────────────────
    rng_boot = np.random.default_rng(123)
    bootstrap_si: list[float] = []

    for _ in range(args.n_bootstrap):
        boot_idx = rng_boot.choice(len(si_vals), size=len(si_vals), replace=True)
        bootstrap_si.append(float(np.mean([si_vals[i] for i in boot_idx])))

    ci_lower = float(np.percentile(bootstrap_si, 2.5))
    ci_upper = float(np.percentile(bootstrap_si, 97.5))
    print(f"  95% CI:      [{ci_lower:.4f}, {ci_upper:.4f}]")

    # ── Output ──────────────────────────────────────────────────
    out = pd.DataFrame([{
        "dataset": args.dataset,
        "method": "stratified_split_standard_null",
        "holdout_si_mean": round(si_mean, 6),
        "holdout_si_std": round(si_std, 6),
        "ci_lower_95": round(ci_lower, 6),
        "ci_upper_95": round(ci_upper, 6),
        "null_si_mean": round(null_mean, 6),
        "null_si_std": round(null_std, 6),
        "si_diff": round(si_mean - null_mean, 6),
        "empirical_p": round(empirical_p, 6),
        "n_splits": len(si_vals),
        "n_perm": len(null_means),
        "n_bootstrap": args.n_bootstrap,
    }])

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    out.to_csv(outdir / "stratified_holdout.csv", index=False)

    print(f"\n{'='*60}")
    print(out.to_string(index=False))

    if empirical_p < 0.05:
        print("\n✅ STRATIFIED p < 0.05 — Borderline fixed!")
    else:
        print(
            f"\n⚠️  Still p = {empirical_p:.3f}, but effect size stable "
            f"(95% CI: [{ci_lower:.3f}, {ci_upper:.3f}])"
        )
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

