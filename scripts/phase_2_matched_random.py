#!/usr/bin/env python3
"""Phase 2 – Matched random sets & sanity check.

For each dataset, verifies that the baseline Separability Index (SI)
from the top-N pathways is meaningfully better than randomly-chosen
pathway sets of the same size.

Procedure:
  1. Load baseline_top_pathways.csv → extract the K selected pathways.
  2. Load pathway_scores.csv + metadata.csv → build IPF vs CTRL arrays.
  3. Compute baseline SI (mean |AUC − 0.5| across K pathways).
  4. Draw n_random random pathway sets of size K, compute SI for each.
  5. Report: baseline_SI, random_mean_SI, random_std_SI, delta, pass/fail.

Pass criterion: baseline_SI − random_mean_SI ≥ margin (default 0.05).

Outputs:
  <outdir>/matched_random_si.csv   – one-row summary
  <outdir>/random_si_distribution.csv – per-iteration random SI values
"""

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def parse_args():
    p = argparse.ArgumentParser(description="Phase 2: matched random sanity check")
    p.add_argument("--dataset", required=True)
    p.add_argument("--metadata", required=True)
    p.add_argument("--scores", required=True)
    p.add_argument("--baseline-pathways", required=True,
                   help="Path to baseline_top_pathways.csv from Phase 1")
    p.add_argument("--unit-col", required=True)
    p.add_argument("--condition-col", default="condition")
    p.add_argument("--ipf-value", default="IPF")
    p.add_argument("--ctrl-value", default="CTRL")
    p.add_argument("--n-random", type=int, default=200,
                   help="Number of random pathway sets to draw")
    p.add_argument("--margin", type=float, default=0.05,
                   help="Minimum delta (baseline − random mean) to pass")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--outdir", required=True)
    return p.parse_args()


def compute_si(ipf_vals: np.ndarray, ctrl_vals: np.ndarray) -> float:
    """Separability Index = mean |AUC − 0.5| across pathways.

    For each pathway, compute the Mann-Whitney U-based AUC between
    IPF and CTRL, then average |AUC − 0.5| over all pathways.
    Higher SI → better separation.
    """
    n_ipf = ipf_vals.shape[0]
    n_ctrl = ctrl_vals.shape[0]
    if n_ipf == 0 or n_ctrl == 0:
        return 0.0

    n_pathways = ipf_vals.shape[1]
    auc_devs = np.zeros(n_pathways)

    for j in range(n_pathways):
        # Mann-Whitney U statistic → AUC
        ipf_col = ipf_vals[:, j]
        ctrl_col = ctrl_vals[:, j]
        # Count: for each IPF value, how many CTRL values it exceeds
        # Using broadcasting (works fine for moderate N)
        u = np.sum(ipf_col[:, None] > ctrl_col[None, :]) + \
            0.5 * np.sum(ipf_col[:, None] == ctrl_col[None, :])
        auc = u / (n_ipf * n_ctrl)
        auc_devs[j] = abs(auc - 0.5)

    return float(np.mean(auc_devs))


def main():
    args = parse_args()

    print(f"[Phase 2] Dataset: {args.dataset}")
    print(f"[Phase 2] Params:  n_random={args.n_random}, margin={args.margin}, seed={args.seed}")

    os.makedirs(args.outdir, exist_ok=True)

    # ── Load inputs ─────────────────────────────────────────────────────
    meta = pd.read_csv(args.metadata)
    scores = pd.read_csv(args.scores)
    baseline_df = pd.read_csv(args.baseline_pathways)

    # Baseline pathway names
    baseline_pathways = list(baseline_df["pathway"])
    k = len(baseline_pathways)
    print(f"[Phase 2] Baseline pathways (K={k}): {baseline_pathways[:5]}...")

    # All pathway columns in scores
    all_pathways = [c for c in scores.columns if c not in ["sample_id", args.unit_col]]
    print(f"[Phase 2] Total pathways in scores: {len(all_pathways)}")

    if k == 0:
        print("[Phase 2] ERROR: no baseline pathways found - cannot proceed")
        sys.exit(1)

    if k > len(all_pathways):
        print(f"[Phase 2] WARNING: K={k} > total pathways={len(all_pathways)}, capping")
        k = len(all_pathways)
        baseline_pathways = baseline_pathways[:k]

    # ── Resolve unit column in scores ───────────────────────────────────
    if args.unit_col in scores.columns:
        id_col = args.unit_col
    elif "sample_id" in scores.columns:
        # Check if sample_id in scores matches unit_col values in metadata
        if set(scores["sample_id"]).intersection(set(meta[args.unit_col])):
            scores = scores.rename(columns={"sample_id": args.unit_col})
            id_col = args.unit_col
        else:
            scores = scores.merge(
                meta[["sample_id", args.unit_col]].drop_duplicates(),
                on="sample_id", how="left"
            )
            id_col = args.unit_col
    else:
        print(f"[Phase 2] ERROR: cannot find unit column '{args.unit_col}' in scores")
        sys.exit(1)

    # ── Split IPF vs CTRL ───────────────────────────────────────────────
    ipf_units = set(
        meta.loc[meta[args.condition_col] == args.ipf_value, args.unit_col].dropna()
    )
    ctrl_units = set(
        meta.loc[meta[args.condition_col] == args.ctrl_value, args.unit_col].dropna()
    )
    print(f"[Phase 2] IPF units: {len(ipf_units)}, CTRL units: {len(ctrl_units)}")

    if len(ipf_units) == 0 or len(ctrl_units) == 0:
        print("[Phase 2] ERROR: need at least 1 unit in each group")
        sys.exit(1)

    # ── Compute baseline SI ─────────────────────────────────────────────
    # Verify all baseline pathways exist in scores
    missing = [p for p in baseline_pathways if p not in all_pathways]
    if missing:
        print(f"[Phase 2] WARNING: {len(missing)} baseline pathways not in scores: {missing[:3]}...")
        baseline_pathways = [p for p in baseline_pathways if p in all_pathways]
        k = len(baseline_pathways)

    ipf_mask = scores[id_col].isin(ipf_units)
    ctrl_mask = scores[id_col].isin(ctrl_units)

    ipf_baseline = scores.loc[ipf_mask, baseline_pathways].values
    ctrl_baseline = scores.loc[ctrl_mask, baseline_pathways].values

    baseline_si = compute_si(ipf_baseline, ctrl_baseline)
    print(f"[Phase 2] Baseline SI: {baseline_si:.4f}")

    # ── Random sets ─────────────────────────────────────────────────────
    rng = np.random.default_rng(args.seed)
    random_sis = []

    for i in range(args.n_random):
        rand_pathways = list(rng.choice(all_pathways, size=k, replace=False))
        ipf_rand = scores.loc[ipf_mask, rand_pathways].values
        ctrl_rand = scores.loc[ctrl_mask, rand_pathways].values
        random_sis.append(compute_si(ipf_rand, ctrl_rand))

    random_sis = np.array(random_sis)
    random_mean = float(np.mean(random_sis))
    random_std = float(np.std(random_sis))
    delta = baseline_si - random_mean
    passed = delta >= args.margin

    print(f"[Phase 2] Random mean SI: {random_mean:.4f} +/- {random_std:.4f}")
    print(f"[Phase 2] Delta (baseline - random mean): {delta:.4f}")
    print(f"[Phase 2] Pass (delta >= {args.margin}): {passed}")

    # ── Empirical p-value: fraction of random ≥ baseline ────────────────
    p_value = float(np.mean(random_sis >= baseline_si))
    print(f"[Phase 2] Empirical p-value (random >= baseline): {p_value:.4f}")

    # ── Write outputs ───────────────────────────────────────────────────
    summary = pd.DataFrame([{
        "dataset": args.dataset,
        "k_pathways": k,
        "baseline_SI": round(baseline_si, 6),
        "random_mean_SI": round(random_mean, 6),
        "random_std_SI": round(random_std, 6),
        "delta": round(delta, 6),
        "margin": args.margin,
        "empirical_p": round(p_value, 4),
        "n_random": args.n_random,
        "pass": passed,
    }])

    summary_path = Path(args.outdir) / "matched_random_si.csv"
    summary.to_csv(summary_path, index=False)
    print(f"[Phase 2] Wrote {summary_path}")

    dist_df = pd.DataFrame({"iteration": range(args.n_random), "random_SI": random_sis})
    dist_path = Path(args.outdir) / "random_si_distribution.csv"
    dist_df.to_csv(dist_path, index=False)
    print(f"[Phase 2] Wrote {dist_path}")

    print(f"[Phase 2] Done: {args.dataset}")


if __name__ == "__main__":
    main()

