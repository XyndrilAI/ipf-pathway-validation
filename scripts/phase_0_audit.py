#!/usr/bin/env python3
"""Phase 0 – Metadata audit.

Reads a metadata CSV and produces a simple audit report:
  - Column presence check
  - Row count
  - Missing-value counts
  - Donor/subject leakage check (are IDs unique to one condition?)

Outputs:
  <outdir>/metadata_audit.csv   – column-level summary
  <outdir>/donor_leakage_audit.csv – per-unit condition mapping
"""

import argparse
import os
import sys
from pathlib import Path

import pandas as pd


def parse_args():
    p = argparse.ArgumentParser(description="Phase 0: metadata audit")
    p.add_argument("--dataset", required=True)
    p.add_argument("--metadata", required=True)
    p.add_argument("--mode", required=True, choices=["bulk", "scrna"])
    p.add_argument("--subject-col", default=None, help="Column for subject ID (bulk)")
    p.add_argument("--donor-col", default=None, help="Column for donor ID (scRNA)")
    p.add_argument("--library-col", default=None, help="Column for library ID (scRNA)")
    p.add_argument("--outdir", required=True)
    return p.parse_args()


def main():
    args = parse_args()

    print(f"[Phase 0] Dataset: {args.dataset}  mode: {args.mode}")
    print(f"[Phase 0] Reading metadata: {args.metadata}")

    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_csv(args.metadata)
    print(f"[Phase 0] Rows: {len(df)}  Columns: {list(df.columns)}")

    # ── Column-level audit ──────────────────────────────────────────────
    audit_rows = []
    for col in df.columns:
        audit_rows.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "non_null": int(df[col].notna().sum()),
            "null": int(df[col].isna().sum()),
            "n_unique": int(df[col].nunique()),
        })
    audit_df = pd.DataFrame(audit_rows)
    audit_path = Path(args.outdir) / "metadata_audit.csv"
    audit_df.to_csv(audit_path, index=False)
    print(f"[Phase 0] Wrote {audit_path}")

    # ── Determine unit column ───────────────────────────────────────────
    unit_col = args.subject_col if args.mode == "bulk" else args.donor_col

    if unit_col is None:
        print(f"[Phase 0] WARNING: unit column not specified, skipping leakage check")
        # Still write an empty leakage file so downstream knows
        leakage_df = pd.DataFrame(columns=["unit_id", "conditions", "n_conditions", "leaked"])
        leakage_path = Path(args.outdir) / "donor_leakage_audit.csv"
        leakage_df.to_csv(leakage_path, index=False)
        print(f"[Phase 0] Wrote (empty) {leakage_path}")
        return

    if unit_col not in df.columns:
        print(f"[Phase 0] WARNING: unit column '{unit_col}' not found in metadata columns {list(df.columns)}")
        leakage_df = pd.DataFrame(columns=["unit_id", "conditions", "n_conditions", "leaked"])
        leakage_path = Path(args.outdir) / "donor_leakage_audit.csv"
        leakage_df.to_csv(leakage_path, index=False)
        print(f"[Phase 0] Wrote (empty) {leakage_path}")
        return

    # ── Donor / subject leakage audit ───────────────────────────────────
    condition_col = "condition"

    if len(df) == 0:
        print(f"[Phase 0] WARNING: metadata has 0 rows – writing empty leakage audit")
        leakage_df = pd.DataFrame(columns=["unit_id", "conditions", "n_conditions", "leaked"])
    elif condition_col not in df.columns:
        print(f"[Phase 0] WARNING: '{condition_col}' column missing – cannot do leakage check")
        leakage_df = pd.DataFrame(columns=["unit_id", "conditions", "n_conditions", "leaked"])
    else:
        grouped = df.groupby(unit_col)[condition_col].apply(
            lambda x: sorted(x.dropna().unique().tolist())
        ).reset_index()
        grouped.columns = ["unit_id", "conditions"]
        grouped["n_conditions"] = grouped["conditions"].apply(len)
        grouped["leaked"] = grouped["n_conditions"] > 1
        grouped["conditions"] = grouped["conditions"].apply(lambda x: ";".join(str(v) for v in x))
        leakage_df = grouped

    leakage_path = Path(args.outdir) / "donor_leakage_audit.csv"
    leakage_df.to_csv(leakage_path, index=False)
    print(f"[Phase 0] Wrote {leakage_path}")

    # Summary
    if len(leakage_df) > 0 and "leaked" in leakage_df.columns:
        n_leaked = int(leakage_df["leaked"].sum())
        print(f"[Phase 0] Leakage summary: {n_leaked}/{len(leakage_df)} units appear in multiple conditions")
    else:
        print(f"[Phase 0] Leakage summary: no data to check")

    print(f"[Phase 0] Done: {args.dataset}")


if __name__ == "__main__":
    main()

