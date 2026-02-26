#!/usr/bin/env python3
"""
Robustness grid: Test sensitivity to TOP_N and random seeds.

Runs LOCO (Leave-One-Subject-Out) SI computation across a grid of
TOP_N values and permutation seeds to show the main finding
(baseline >> null) is not parameter-dependent.

Outputs per dataset:
  <outdir>/robustness_grid.csv     – full grid (TOP_N × seed)
  <outdir>/robustness_summary.csv  – summary aggregated by TOP_N
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


# ── Core functions (self-contained, same logic as phase_3_holdout) ──────

def jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity between two sets."""
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


def topN_pathways(effect: pd.Series, top_n: int) -> set[str]:
    """Return top-N pathway names by absolute effect size."""
    return set(effect.abs().sort_values(ascending=False).head(top_n).index)


def compute_effect(path_scores: pd.DataFrame, labels) -> pd.Series:
    """Mean(IPF) - Mean(CTRL) per pathway."""
    ipf = path_scores[labels == 1].mean(axis=0)
    ctrl = path_scores[labels == 0].mean(axis=0)
    return ipf - ctrl


def loco_si(
    df: pd.DataFrame,
    scores: pd.DataFrame,
    unit_col: str,
    label_col: str,
    top_n: int,
) -> list[float]:
    """Leave-One-Subject-Out Separability Index.

    For each subject, compute effect on the remaining subjects (train)
    and on the full set, then measure Jaccard between train top-N
    and full-data top-N.
    """
    units = df[unit_col].dropna().unique()
    labels = df[label_col].values

    # Full-data effect (reference)
    full_effect = compute_effect(scores, labels)
    full_top = topN_pathways(full_effect, top_n)

    si_vals: list[float] = []
    for u in units:
        mask = df[unit_col] != u
        if mask.sum() == 0:
            continue
        train_effect = compute_effect(scores.loc[mask], labels[mask])
        train_top = topN_pathways(train_effect, top_n)
        si_vals.append(jaccard(train_top, full_top))

    return si_vals


# ── Main ────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Robustness grid: sensitivity to TOP_N and random seeds"
    )
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--metadata", required=True)
    ap.add_argument("--scores", required=True)
    ap.add_argument("--unit-col", required=True)
    ap.add_argument("--condition-col", default="condition")
    ap.add_argument("--ipf-value", default="IPF")
    ap.add_argument("--ctrl-value", default="CTRL")
    ap.add_argument("--top-n-values", default="10,20,50",
                    help="Comma-separated TOP_N values to test")
    ap.add_argument("--seeds", type=int, default=5,
                    help="Number of independent permutation seeds")
    ap.add_argument("--n-perm", type=int, default=100,
                    help="Permutations per seed (100 for fast test, 500 for full)")
    ap.add_argument("--outdir", default=".")
    args = ap.parse_args()

    top_n_values = [int(x) for x in args.top_n_values.split(",")]

    # ── Load & merge ────────────────────────────────────────────────
    md = pd.read_csv(args.metadata)
    sc = pd.read_csv(args.scores)

    if "sample_id" not in md.columns or "sample_id" not in sc.columns:
        raise SystemExit("Both metadata and scores must contain sample_id")

    df = md.merge(sc, on="sample_id", how="inner")

    cond = df[args.condition_col].astype(str)
    y = np.where(
        cond == args.ipf_value, 1,
        np.where(cond == args.ctrl_value, 0, np.nan),
    )
    if np.isnan(y).any():
        raise SystemExit(
            f"Condition values must be '{args.ipf_value}' or "
            f"'{args.ctrl_value}'. Found: {cond.unique()}"
        )
    df["_y"] = y.astype(int)

    # Identify pathway score columns
    score_cols = [
        c for c in df.columns
        if c not in md.columns and c not in ("sample_id", "_y", "_y_perm")
    ]
    scores = df[score_cols].apply(pd.to_numeric, errors="coerce")
    scores = scores.dropna(axis=1, how="all")

    if scores.shape[1] == 0:
        raise SystemExit("No numeric pathway score columns found")

    n_units = df[args.unit_col].nunique()
    print(f"\n{'='*60}")
    print(f"  Robustness Grid: {args.dataset}")
    print(f"  Units: {n_units}   Pathways: {scores.shape[1]}")
    print(f"  TOP_N values: {top_n_values}")
    print(f"  Seeds: {args.seeds}   Perms/seed: {args.n_perm}")
    print(f"{'='*60}")

    # ── Grid computation ────────────────────────────────────────────
    results: list[dict] = []

    for top_n in top_n_values:
        # LOCO baseline (deterministic – same for every seed)
        si_vals = loco_si(df, scores, args.unit_col, "_y", top_n)
        si_mean = float(np.mean(si_vals)) if si_vals else float("nan")
        si_std = float(np.std(si_vals)) if si_vals else float("nan")

        for seed_idx in range(args.seeds):
            rng = np.random.default_rng(seed_idx)

            null_si_list: list[float] = []
            for _ in range(args.n_perm):
                perm = df["_y"].to_numpy().copy()
                rng.shuffle(perm)
                df["_y_perm"] = perm
                vals = loco_si(df, scores, args.unit_col, "_y_perm", top_n)
                if vals:
                    null_si_list.append(float(np.mean(vals)))

            null_arr = np.array(null_si_list)
            null_mean = float(null_arr.mean()) if len(null_arr) else float("nan")
            empirical_p = (
                float(np.mean(null_arr >= si_mean))
                if len(null_arr)
                else float("nan")
            )

            print(
                f"  [TOP_N={top_n:>3}, seed={seed_idx}]  "
                f"SI={si_mean:.3f}±{si_std:.3f}  "
                f"null={null_mean:.3f}  p={empirical_p:.4f}"
            )

            results.append({
                "dataset": args.dataset,
                "top_n": top_n,
                "seed": seed_idx,
                "si_mean": round(si_mean, 6),
                "si_std": round(si_std, 6),
                "null_mean": round(null_mean, 6),
                "si_diff": round(si_mean - null_mean, 6),
                "empirical_p": round(empirical_p, 6),
                "n_folds": len(si_vals),
                "n_perm": len(null_si_list),
            })

    # ── Save full grid ──────────────────────────────────────────────
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    results_df = pd.DataFrame(results)
    results_df.to_csv(outdir / "robustness_grid.csv", index=False)

    # ── Summary by TOP_N ────────────────────────────────────────────
    summary = (
        results_df
        .groupby("top_n")
        .agg(
            si_mean_avg=("si_mean", "mean"),
            si_mean_sd=("si_mean", "std"),
            null_mean_avg=("null_mean", "mean"),
            null_mean_sd=("null_mean", "std"),
            si_diff_avg=("si_diff", "mean"),
            si_diff_sd=("si_diff", "std"),
            empirical_p_avg=("empirical_p", "mean"),
            empirical_p_sd=("empirical_p", "std"),
        )
        .reset_index()
    )
    summary.to_csv(outdir / "robustness_summary.csv", index=False)

    print(f"\n{'='*60}")
    print("  Summary Across Seeds")
    print(f"{'='*60}")
    print(summary.to_string(index=False))

    print(f"\n✅ Results saved to {outdir}")
    print(f"   robustness_grid.csv    ({len(results_df)} rows)")
    print(f"   robustness_summary.csv ({len(summary)} rows)")


if __name__ == "__main__":
    main()

