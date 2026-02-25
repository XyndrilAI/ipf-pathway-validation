#!/usr/bin/env python3
"""Phase 3 - Holdout validation (subject-level split).

For each dataset, repeatedly splits subjects into train/test,
computes top-N pathways on train, measures Jaccard stability on test,
and compares to a permutation null.

Outputs:
  <outdir>/holdout_si.csv - one-row summary
"""
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
from pathlib import Path


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def topN_pathways(effect: pd.Series, top_n: int) -> set[str]:
    return set(effect.abs().sort_values(ascending=False).head(top_n).index)


def compute_effect(path_scores: pd.DataFrame, labels: pd.Series) -> pd.Series:
    ipf = path_scores[labels == 1].mean(axis=0)
    ctrl = path_scores[labels == 0].mean(axis=0)
    return ipf - ctrl


def holdout_split_si(md: pd.DataFrame, scores: pd.DataFrame, unit_col: str, label_col: str,
                     top_n: int, train_frac: float = 0.7, rng: np.random.Generator = None) -> float:
    """Single random holdout split."""
    if rng is None:
        rng = np.random.default_rng()

    units = md[unit_col].dropna().unique()
    n_train = max(1, int(len(units) * train_frac))

    train_units = rng.choice(units, size=n_train, replace=False)
    train_idx = md[unit_col].isin(train_units)
    test_idx = ~train_idx

    if test_idx.sum() == 0 or train_idx.sum() == 0:
        return np.nan

    eff_train = compute_effect(scores.loc[train_idx], md.loc[train_idx, label_col])
    eff_test = compute_effect(scores.loc[test_idx], md.loc[test_idx, label_col])

    return jaccard(topN_pathways(eff_train, top_n), topN_pathways(eff_test, top_n))


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase 3: holdout validation")
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
    ap.add_argument("--train-frac", type=float, default=0.7)
    ap.add_argument("--outdir", default=".")
    args = ap.parse_args()

    print(f"[Phase 3] Dataset: {args.dataset}")
    print(f"[Phase 3] Params:  top_n={args.top_n}, n_splits={args.n_splits}, "
          f"n_perm={args.n_perm}, train_frac={args.train_frac}")

    md = pd.read_csv(args.metadata)
    sc = pd.read_csv(args.scores)

    if "sample_id" not in md.columns or "sample_id" not in sc.columns:
        raise SystemExit("Both metadata and scores must contain sample_id")

    df = md.merge(sc, on="sample_id", how="inner")

    print(f"[Phase 3] Merged rows: {len(df)}, Metadata: {len(md)}, Scores: {len(sc)}")

    cond = df[args.condition_col].astype(str)
    y = np.where(cond == args.ipf_value, 1, np.where(cond == args.ctrl_value, 0, np.nan))
    if np.isnan(y).any():
        raise SystemExit(f"Condition values must match IPF/CTRL. Found: {cond.unique()}")

    df["_y"] = y.astype(int)

    # Score columns
    score_cols = [c for c in df.columns if c not in md.columns]
    score_cols = [c for c in score_cols if c not in ["sample_id", "_y", "_y_perm"]]
    scores = df[score_cols].apply(pd.to_numeric, errors="coerce")
    scores = scores.dropna(axis=1, how="all")

    if scores.shape[1] == 0:
        raise SystemExit("No numeric pathway score columns found")

    print(f"[Phase 3] Using {scores.shape[1]} pathway scores, "
          f"{df[args.unit_col].nunique()} units")

    # --- Holdout splits --------------------------------------------------
    rng = np.random.default_rng(42)
    si_vals = []

    for i in range(args.n_splits):
        si = holdout_split_si(df, scores, args.unit_col, "_y",
                              args.top_n, args.train_frac, rng)
        if not np.isnan(si):
            si_vals.append(si)

    si_mean = float(np.mean(si_vals)) if si_vals else float("nan")
    si_std = float(np.std(si_vals)) if si_vals else float("nan")

    print(f"[Phase 3] Holdout SI: {si_mean:.4f} +/- {si_std:.4f}  "
          f"({len(si_vals)}/{args.n_splits} valid splits)")

    # --- Permutation null ------------------------------------------------
    null_means = []
    rng_null = np.random.default_rng(0)

    for p_i in range(args.n_perm):
        perm = df["_y"].to_numpy().copy()
        rng_null.shuffle(perm)
        df["_y_perm"] = perm

        si = holdout_split_si(df, scores, args.unit_col, "_y_perm",
                              args.top_n, args.train_frac, rng)
        if not np.isnan(si):
            null_means.append(si)

    null_mean = float(np.mean(null_means)) if null_means else float("nan")
    null_std = float(np.std(null_means)) if null_means else float("nan")
    empirical_p = (float(np.mean(np.array(null_means) >= si_mean))
                   if null_means else float("nan"))

    print(f"[Phase 3] Null SI:    {null_mean:.4f} +/- {null_std:.4f}  "
          f"({len(null_means)} perms)")
    print(f"[Phase 3] Delta:      {si_mean - null_mean:.4f}")
    print(f"[Phase 3] Empirical p: {empirical_p:.4f}")

    # --- Output ----------------------------------------------------------
    out = pd.DataFrame([{
        "dataset": args.dataset,
        "holdout_si_mean": round(si_mean, 6),
        "holdout_si_std": round(si_std, 6),
        "null_si_mean": round(null_mean, 6),
        "null_si_std": round(null_std, 6),
        "si_diff": round(si_mean - null_mean, 6),
        "empirical_p": round(empirical_p, 4),
        "n_splits": len(si_vals),
        "n_perm": len(null_means),
        "top_n": args.top_n,
        "train_frac": args.train_frac,
    }])

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    out_path = outdir / "holdout_si.csv"
    out.to_csv(out_path, index=False)
    print(f"[Phase 3] Wrote {out_path}")

    print("\n=== HOLDOUT RESULTS ===")
    print(out.to_string(index=False))

    # Quick decision guide
    if empirical_p < 0.05 and si_mean - null_mean > 0.05:
        print("\n>> HOLDOUT PASS - Signal robust to generalization")
    else:
        print("\n>> HOLDOUT WEAK - Consider Path C or additional data")

    print(f"[Phase 3] Done: {args.dataset}")


if __name__ == "__main__":
    main()

