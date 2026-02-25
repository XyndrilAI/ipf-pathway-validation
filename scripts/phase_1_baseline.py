#!/usr/bin/env python3
"""Phase 1 – Baseline pathway analysis.

Reads metadata + pathway_scores and produces:
  - Top-N differentially active pathways (IPF vs CTRL)
  - Permutation-based p-values
  - Summary CSV

This is a placeholder that will be expanded with real statistical logic.
"""

import argparse
import os
import sys
from pathlib import Path

import pandas as pd
import numpy as np


def parse_args():
    p = argparse.ArgumentParser(description="Phase 1: baseline pathway analysis")
    p.add_argument("--dataset", required=True)
    p.add_argument("--metadata", required=True)
    p.add_argument("--scores", required=True)
    p.add_argument("--unit-col", required=True)
    p.add_argument("--condition-col", required=True)
    p.add_argument("--ipf-value", required=True)
    p.add_argument("--ctrl-value", required=True)
    p.add_argument("--top-n", type=int, default=20)
    p.add_argument("--n-perm", type=int, default=500)
    p.add_argument("--outdir", required=True)
    return p.parse_args()


def main():
    args = parse_args()

    print(f"[Phase 1] Dataset: {args.dataset}")
    print(f"[Phase 1] Scores:  {args.scores}")
    print(f"[Phase 1] Params:  unit={args.unit_col}, condition={args.condition_col}, "
          f"IPF={args.ipf_value}, CTRL={args.ctrl_value}, top_n={args.top_n}, n_perm={args.n_perm}")

    os.makedirs(args.outdir, exist_ok=True)

    meta = pd.read_csv(args.metadata)
    scores = pd.read_csv(args.scores)

    print(f"[Phase 1] Metadata rows: {len(meta)}, Scores shape: {scores.shape}")

    # Validate required columns
    missing_meta = [c for c in [args.unit_col, args.condition_col] if c not in meta.columns]
    if missing_meta:
        print(f"[Phase 1] WARNING: metadata missing columns: {missing_meta}")
        # Write empty result
        result = pd.DataFrame(columns=["pathway", "mean_ipf", "mean_ctrl", "diff", "perm_pvalue"])
        out_path = Path(args.outdir) / "baseline_top_pathways.csv"
        result.to_csv(out_path, index=False)
        print(f"[Phase 1] Wrote (empty) {out_path}")
        return

    # Filter to IPF and CTRL
    ipf_units = set(meta.loc[meta[args.condition_col] == args.ipf_value, args.unit_col].dropna())
    ctrl_units = set(meta.loc[meta[args.condition_col] == args.ctrl_value, args.unit_col].dropna())

    print(f"[Phase 1] IPF units: {len(ipf_units)}, CTRL units: {len(ctrl_units)}")

    if len(ipf_units) == 0 or len(ctrl_units) == 0:
        print(f"[Phase 1] WARNING: not enough units in both groups for comparison")
        result = pd.DataFrame(columns=["pathway", "mean_ipf", "mean_ctrl", "diff", "perm_pvalue"])
        out_path = Path(args.outdir) / "baseline_top_pathways.csv"
        result.to_csv(out_path, index=False)
        print(f"[Phase 1] Wrote (empty) {out_path}")
        return

    # Resolve unit column in scores: scores always has 'sample_id'; metadata maps sample_id -> unit_col
    # If unit_col == 'sample_id' or unit_col is already in scores, use directly.
    # Otherwise, join via metadata to map sample_id -> unit_col.
    if args.unit_col in scores.columns:
        id_col_in_scores = args.unit_col
    elif "sample_id" in scores.columns:
        # Map: in metadata, sample_id == unit_col values (aggregated case),
        # or merge scores with metadata to get unit_col
        if set(scores["sample_id"]).intersection(meta[args.unit_col]):
            # sample_id in scores matches unit_col in metadata (aggregated data)
            scores = scores.rename(columns={"sample_id": args.unit_col})
            id_col_in_scores = args.unit_col
        else:
            # Need to merge to get unit_col
            scores = scores.merge(meta[["sample_id", args.unit_col]], on="sample_id", how="left")
            id_col_in_scores = args.unit_col
    else:
        print(f"[Phase 1] WARNING: neither '{args.unit_col}' nor 'sample_id' in scores columns {list(scores.columns)}")
        result = pd.DataFrame(columns=["pathway", "mean_ipf", "mean_ctrl", "diff", "perm_pvalue"])
        out_path = Path(args.outdir) / "baseline_top_pathways.csv"
        result.to_csv(out_path, index=False)
        print(f"[Phase 1] Wrote (empty) {out_path}")
        return

    pathway_cols = [c for c in scores.columns if c not in [id_col_in_scores, "sample_id"]]

    ipf_scores = scores[scores[id_col_in_scores].isin(ipf_units)][pathway_cols]
    ctrl_scores = scores[scores[id_col_in_scores].isin(ctrl_units)][pathway_cols]

    # Mean difference per pathway
    mean_ipf = ipf_scores.mean()
    mean_ctrl = ctrl_scores.mean()
    diff = mean_ipf - mean_ctrl

    # Permutation test
    all_scores = scores[scores[id_col_in_scores].isin(ipf_units | ctrl_units)]
    all_vals = all_scores[pathway_cols].values
    all_labels = all_scores[id_col_in_scores].isin(ipf_units).values  # True=IPF

    n_ipf = int(all_labels.sum())
    rng = np.random.default_rng(42)

    perm_counts = np.zeros(len(pathway_cols))

    for _ in range(args.n_perm):
        perm_labels = rng.permutation(all_labels)
        perm_diff = all_vals[perm_labels].mean(axis=0) - all_vals[~perm_labels].mean(axis=0)
        perm_counts += (np.abs(perm_diff) >= np.abs(diff.values))

    perm_pvalues = (perm_counts + 1) / (args.n_perm + 1)

    # Build result
    result = pd.DataFrame({
        "pathway": pathway_cols,
        "mean_ipf": mean_ipf.values,
        "mean_ctrl": mean_ctrl.values,
        "diff": diff.values,
        "perm_pvalue": perm_pvalues,
    })
    result = result.sort_values("perm_pvalue").head(args.top_n)

    out_path = Path(args.outdir) / "baseline_top_pathways.csv"
    result.to_csv(out_path, index=False)
    print(f"[Phase 1] Wrote {out_path} ({len(result)} pathways)")

    print(f"[Phase 1] Done: {args.dataset}")


if __name__ == "__main__":
    main()

