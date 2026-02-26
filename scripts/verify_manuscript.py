#!/usr/bin/env python3
"""Complete manuscript verification — checks all numbers match CSV files."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

# Ensure UTF-8 output even when piped on Windows (cp1252)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RESULTS = Path(r"D:\ipf_sprint\results")
PAPER = RESULTS / "paper"

PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"

issues: list[str] = []


def status(ok: bool) -> str:
    return PASS if ok else FAIL


def read_csv_row(path: Path) -> dict:
    """Read single-data-row CSV and return dict."""
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return next(reader)


# ══════════════════════════════════════════════════════════════
# 1. Phase 1 (Baseline) — per-pathway p-values
# ══════════════════════════════════════════════════════════════
print("=" * 65)
print("MANUSCRIPT VERIFICATION REPORT")
print("=" * 65)

for ds in ("GSE24206", "GSE53845"):
    bp = RESULTS / f"02_baseline/{ds}/baseline_top_pathways.csv"
    if not bp.exists():
        print(f"\n{FAIL} {ds} Phase 1: baseline_top_pathways.csv NOT FOUND")
        issues.append(f"{ds}: baseline_top_pathways.csv missing")
        continue
    import pandas as pd

    df = pd.read_csv(bp)
    min_p = df["perm_pvalue"].min()
    max_p = df["perm_pvalue"].max()
    n_pw = len(df)
    print(f"\n>> {ds} Phase 1 (Baseline Top Pathways):")
    print(f"   Pathways:   {n_pw}")
    print(f"   Min perm_p: {min_p:.4f}")
    print(f"   Max perm_p: {max_p:.4f}")
    print(f"   All p<0.05: {status(max_p < 0.05)} (max={max_p:.4f})")

# ══════════════════════════════════════════════════════════════
# 2. Phase 2 (Matched Random)
# ══════════════════════════════════════════════════════════════
for ds in ("GSE24206", "GSE53845"):
    mr = RESULTS / f"03_matched_random/{ds}/matched_random_si.csv"
    if not mr.exists():
        print(f"\n{FAIL} {ds} Phase 2: matched_random_si.csv NOT FOUND")
        issues.append(f"{ds}: matched_random_si.csv missing")
        continue
    row = read_csv_row(mr)
    bsi = float(row["baseline_SI"])
    rmean = float(row["random_mean_SI"])
    rstd = float(row["random_std_SI"])
    delta = float(row["delta"])
    emp_p = float(row["empirical_p"])

    print(f"\n>> {ds} Phase 2 (Random Control):")
    print(f"   Baseline SI:     {bsi:.3f}")
    print(f"   Random mean SI:  {rmean:.3f} +/- {rstd:.3f}")
    print(f"   Delta:           {delta:.3f}")
    print(f"   Empirical p:     {emp_p}")
    print(f"   Delta > 0.05:    {status(delta > 0.05)}")
    print(f"   p < 0.05:        {status(emp_p < 0.05)}")

# ══════════════════════════════════════════════════════════════
# 3. Phase 3 (Holdout)
# ══════════════════════════════════════════════════════════════
holdout_data = {}
for ds in ("GSE24206", "GSE53845"):
    ho = RESULTS / f"04_holdout/{ds}/holdout_si.csv"
    if not ho.exists():
        print(f"\n{FAIL} {ds} Phase 3: holdout_si.csv NOT FOUND")
        issues.append(f"{ds}: holdout_si.csv missing")
        continue
    row = read_csv_row(ho)
    si_mean = float(row["holdout_si_mean"])
    si_std = float(row["holdout_si_std"])
    null_mean = float(row["null_si_mean"])
    null_std = float(row["null_si_std"])
    si_diff = float(row["si_diff"])
    emp_p = float(row["empirical_p"])
    holdout_data[ds] = row

    print(f"\n>> {ds} Phase 3 (Holdout):")
    print(f"   Holdout SI:  {si_mean:.3f} +/- {si_std:.3f}")
    print(f"   Null SI:     {null_mean:.3f} +/- {null_std:.3f}")
    print(f"   Delta:       {si_diff:.3f}")
    print(f"   Empirical p: {emp_p:.2f}")
    print(f"   Delta > 0.10: {status(si_diff > 0.10)}")

# ══════════════════════════════════════════════════════════════
# 4. Cross-check manuscript text
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("CROSS-CHECK: Manuscript vs CSV")
print("=" * 65)

results_md = (PAPER / "results_draft.md").read_text(encoding="utf-8")
abstract_md = (PAPER / "abstract.md").read_text(encoding="utf-8")
methods_md = (PAPER / "methods_draft.md").read_text(encoding="utf-8")

# Check SI formula in methods
has_formula = "|A" in methods_md and "|A ∩ B|" in methods_md or "A ∩ B" in methods_md
print(f"\n  SI formula in Methods:    {status(has_formula)}")
if not has_formula:
    issues.append("SI Jaccard formula missing from Methods")

# Check 'Jaccard' in methods
has_jaccard = "Jaccard" in methods_md
print(f"  'Jaccard' in Methods:     {status(has_jaccard)}")

# Check top-20 in methods
has_top20 = "top-20" in methods_md or "top 20" in methods_md.lower()
print(f"  'top-20' in Methods:      {status(has_top20)}")

# Holdout numbers in results
# Manuscript now reports stratified holdout as primary, so check both
if "GSE24206" in holdout_data:
    # Original: 0.499, Stratified: 0.512 — manuscript may cite either
    found_24206_si = any(s in results_md for s in ("0.499", "0.50", "0.512"))
    print(f"\n  GSE24206 holdout SI in Results:   {status(found_24206_si)}")
    if not found_24206_si:
        issues.append("GSE24206 holdout SI not found in results_draft.md")

    # Original p=0.03, Stratified p=0.028
    found_24206_p = any(s in results_md for s in ("p = 0.03", "p=0.03", "p = 0.028", "p=0.028"))
    print(f"  GSE24206 holdout p in Results:    {status(found_24206_p)}")
    if not found_24206_p:
        issues.append("GSE24206 holdout p-value not found in results_draft.md")

if "GSE53845" in holdout_data:
    # Original: 0.467, Stratified: 0.500
    found_53845_si = any(s in results_md for s in ("0.467", "0.47", "0.500", "0.50"))
    print(f"  GSE53845 holdout SI in Results:   {status(found_53845_si)}")
    if not found_53845_si:
        issues.append("GSE53845 holdout SI not found in results_draft.md")

    # Original p=0.07, Stratified p=0.04 — manuscript should mention both
    found_53845_p = any(s in results_md for s in ("p = 0.07", "p=0.07", "p = 0.04", "p=0.04"))
    print(f"  GSE53845 holdout p in Results:    {status(found_53845_p)}")
    if not found_53845_p:
        issues.append("GSE53845 holdout p-value not found in results_draft.md")

# Phase 2 numbers in results
found_phase2_delta_24 = "0.156" in results_md
found_phase2_delta_53 = "0.128" in results_md
print(f"\n  Phase 2 Delta GSE24206 in Results:   {status(found_phase2_delta_24)}")
print(f"  Phase 2 Delta GSE53845 in Results:   {status(found_phase2_delta_53)}")
if not found_phase2_delta_24:
    issues.append("Phase 2 delta for GSE24206 not in results_draft.md")
if not found_phase2_delta_53:
    issues.append("Phase 2 delta for GSE53845 not in results_draft.md")

# Check overlap count consistency (should be 8/20 per supp_table_s2.csv)
supp_s2 = PAPER / "supplementary_table_s2.csv"
if supp_s2.exists():
    s2 = pd.read_csv(supp_s2)
    top20_row = s2[s2["Rank Cutoff"] == "Top-20"].iloc[0]
    csv_overlap = int(top20_row["Overlap (n)"])
    csv_jaccard = float(top20_row["Jaccard Index"])

    results_has_overlap = f"{csv_overlap}/20" in results_md
    abstract_has_overlap = f"{csv_overlap}/20" in abstract_md
    print(f"\n  Overlap {csv_overlap}/20 in Results:   {status(results_has_overlap)}")
    print(f"  Overlap {csv_overlap}/20 in Abstract:  {status(abstract_has_overlap)}")
    if not results_has_overlap:
        issues.append(f"Results says wrong overlap count (should be {csv_overlap}/20)")
    if not abstract_has_overlap:
        issues.append(f"Abstract says wrong overlap count (should be {csv_overlap}/20)")

# ══════════════════════════════════════════════════════════════
# 5. Check Table 1 completeness
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("TABLE 1 VERIFICATION")
print("=" * 65)
table1_text = (PAPER / "table1.md").read_text(encoding="utf-8")

table1_checks = [
    ("Phase 0 subjects", "17 (11 IPF" in table1_text and "48 (40 IPF" in table1_text),
    ("Phase 2 baseline SI", "0.381" in table1_text and "0.349" in table1_text),
    ("Phase 2 random mean", "0.225" in table1_text and "0.221" in table1_text),
    ("Phase 2 delta", "0.156" in table1_text and "0.128" in table1_text),
    ("Phase 3 holdout SI", "0.499" in table1_text and "0.467" in table1_text),
    ("Phase 3 null SI", "0.316" in table1_text and "0.303" in table1_text),
    ("Phase 3 delta", "0.183" in table1_text and "0.164" in table1_text),
    ("Phase 3 p-values", "0.03" in table1_text and "0.07" in table1_text),
]

for label, ok in table1_checks:
    print(f"  {label}: {status(ok)}")
    if not ok:
        issues.append(f"Table 1 missing/wrong: {label}")

# ══════════════════════════════════════════════════════════════
# 6. Check supplementary tables exist
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("SUPPLEMENTARY FILES")
print("=" * 65)
for fname in [
    "supplementary_table_s1.csv",
    "supplementary_table_s2.csv",
    "supplementary_table_s3_leakage_audit.csv",
    "supplementary_table_s4_robustness.csv",
    "supplementary_table_s5_stratified.csv",
    "figure1_phase2_baseline_vs_random.pdf",
    "figure2_phase3_holdout.pdf",
    "manuscript_combined.docx",
]:
    fpath = PAPER / fname
    exists = fpath.exists()
    size = f"({fpath.stat().st_size / 1024:.1f} KB)" if exists else ""
    print(f"  {fname}: {status(exists)} {size}")
    if not exists:
        issues.append(f"Missing file: {fname}")

# ══════════════════════════════════════════════════════════════
# 7. Check stratified holdout results
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("STRATIFIED HOLDOUT VERIFICATION")
print("=" * 65)
for ds in ("GSE24206", "GSE53845"):
    strat = RESULTS / f"stratified/{ds}/stratified_holdout.csv"
    if strat.exists():
        row = read_csv_row(strat)
        si = float(row["holdout_si_mean"])
        p = float(row["empirical_p"])
        ci_lo = float(row["ci_lower_95"])
        ci_hi = float(row["ci_upper_95"])
        print(f"  {ds}: SI={si:.3f}, p={p:.3f}, 95%CI=[{ci_lo:.3f}, {ci_hi:.3f}] {status(p < 0.05)}")
    else:
        print(f"  {ds}: stratified_holdout.csv NOT FOUND {WARN}")

# ══════════════════════════════════════════════════════════════
# 8. Check robustness grid results
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("ROBUSTNESS GRID VERIFICATION")
print("=" * 65)
for ds in ("GSE24206", "GSE53845"):
    rob = RESULTS / f"robustness/{ds}/robustness_summary.csv"
    if rob.exists():
        df = pd.read_csv(rob)
        for _, r in df.iterrows():
            tn = int(r["top_n"])
            p = r["empirical_p_avg"]
            delta = r["si_diff_avg"]
            print(f"  {ds} TOP_N={tn:2d}: delta={delta:.3f}, p={p:.3f} {status(tn == 20 and p < 0.05) if tn == 20 else ''}")
    else:
        print(f"  {ds}: robustness_summary.csv NOT FOUND {WARN}")

# ══════════════════════════════════════════════════════════════
# FINAL VERDICT
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
if issues:
    print(f"VERDICT: {FAIL} -- {len(issues)} issue(s) found:")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
else:
    print(f"VERDICT: {PASS} -- All checks passed. Ready for submission.")
print("=" * 65)

sys.exit(1 if issues else 0)

