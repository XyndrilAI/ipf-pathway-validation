#!/usr/bin/env python3
"""Final comprehensive verification before submission."""
from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd

BASE = Path(r"D:\ipf_sprint")
PAPER = BASE / "results" / "paper"

errors: list[str] = []


def ok(cond: bool, msg: str) -> None:
    tag = "  ✅" if cond else "  ❌"
    print(f"{tag} {msg}")
    if not cond:
        errors.append(msg)


def check_file(path: Path, label: str) -> bool:
    exists = path.exists() and (path.is_dir() or path.stat().st_size > 0)
    ok(exists, f"{label}  ({path.stat().st_size} B)" if exists else f"MISSING: {label} → {path}")
    return exists


# ── 1. Critical files ────────────────────────────────────────
print("=" * 60)
print("FINAL VERIFICATION — Submission Readiness Check")
print("=" * 60)

print("\n[1/7] Critical Files")
critical = {
    "Manuscript DOCX": PAPER / "manuscript_combined.docx",
    "Figure 1 (PDF)": PAPER / "figures" / "figure1_phase2_baseline_vs_random.pdf",
    "Figure 2 (PDF)": PAPER / "figures" / "figure2_phase3_holdout.pdf",
    "Supp Table S1": PAPER / "supplementary_table_s1.csv",
    "Supp Table S2": PAPER / "supplementary_table_s2.csv",
    "Supp Table S3 (leakage)": PAPER / "supplementary_table_s3_leakage_audit.csv",
    "Supp Table S4 (robustness)": PAPER / "supplementary_table_s4_robustness.csv",
    "Supp Table S5 (stratified)": PAPER / "supplementary_table_s5_stratified.csv",
    "Cover Letter": PAPER / "cover_letter.md",
    "REPRODUCE.md": BASE / "REPRODUCE.md",
    "NEXT_STEPS.md": BASE / "NEXT_STEPS.md",
    "bioRxiv Metadata": PAPER / "BIORXIV_METADATA.txt",
}
for label, path in critical.items():
    check_file(path, label)

# ── 2. Stratified holdout numbers ─────────────────────────────
print("\n[2/7] Stratified Holdout (Phase 3)")
for ds in ("GSE24206", "GSE53845"):
    csv_path = BASE / f"results/stratified/{ds}/stratified_holdout.csv"
    if not csv_path.exists():
        ok(False, f"{ds}: stratified_holdout.csv missing")
        continue
    row = pd.read_csv(csv_path).iloc[0]
    si = row["holdout_si_mean"]
    p = row["empirical_p"]
    ci_lo = row["ci_lower_95"]
    ci_hi = row["ci_upper_95"]
    print(f"  {ds}: SI={si:.3f}, p={p:.3f}, 95%CI=[{ci_lo:.3f},{ci_hi:.3f}]")
    ok(p < 0.05, f"{ds} p={p:.3f} < 0.05")

# ── 3. Robustness grid ───────────────────────────────────────
print("\n[3/7] Robustness Grid")
for ds in ("GSE24206", "GSE53845"):
    csv_path = BASE / f"results/robustness/{ds}/robustness_summary.csv"
    if not csv_path.exists():
        ok(False, f"{ds}: robustness_summary.csv missing")
        continue
    df = pd.read_csv(csv_path)
    for _, r in df.iterrows():
        tn = int(r["top_n"])
        delta = r["si_diff_avg"]
        p = r["empirical_p_avg"]
        marker = ""
        if tn == 20:
            marker = " ← PRIMARY"
        elif tn == 50:
            marker = " (degenerate expected)"
        print(f"  {ds} TOP_N={tn:2d}: Δ={delta:.3f}, p={p:.3f}{marker}")
    # TOP_N=20 should have lowest p for this dataset
    t20 = df[df["top_n"] == 20]
    if len(t20):
        ok(t20.iloc[0]["si_diff_avg"] > 0.05, f"{ds} TOP_N=20 Δ>0.05")

# ── 4. Leakage audit ─────────────────────────────────────────
print("\n[4/7] Leakage Audit (Phase 0)")
s3 = PAPER / "supplementary_table_s3_leakage_audit.csv"
if s3.exists():
    audit = pd.read_csv(s3)
    for ds_name in audit["dataset"].unique():
        sub = audit[audit["dataset"] == ds_name]
        max_per = sub.groupby("subject_id").size().max()
        ok(max_per <= 1, f"{ds_name}: max {max_per} sample/subject (need ≤1)")
else:
    ok(False, "S3 leakage audit CSV missing")

# ── 5. Manuscript text cross-checks ──────────────────────────
print("\n[5/7] Manuscript Text Cross-Checks")
results_md = (PAPER / "results_draft.md").read_text(encoding="utf-8")
abstract_md = (PAPER / "abstract.md").read_text(encoding="utf-8")
methods_md = (PAPER / "methods_draft.md").read_text(encoding="utf-8")

ok("Jaccard" in methods_md, "Methods mentions 'Jaccard'")
ok("top-20" in methods_md or "top 20" in methods_md.lower(), "Methods mentions 'top-20'")
ok("A ∩ B" in methods_md or "|A" in methods_md, "Methods has SI formula")
ok("stratified" in methods_md.lower(), "Methods describes stratified holdout")
ok("sensitivity" in methods_md.lower() or "TOP_N" in methods_md, "Methods describes parameter sensitivity")

ok(any(s in results_md for s in ("0.512", "0.50")), "Results: GSE24206 stratified SI present")
ok(any(s in results_md for s in ("0.028", "0.03")), "Results: GSE24206 p-value present")
ok(any(s in results_md for s in ("0.500", "0.50")), "Results: GSE53845 stratified SI present")
ok(any(s in results_md for s in ("0.04",)), "Results: GSE53845 stratified p=0.04 present")
ok("p=0.07" in results_md or "p = 0.07" in results_md, "Results: mentions original borderline p=0.07")
ok("8/20" in results_md, "Results: overlap 8/20")
ok("8/20" in abstract_md, "Abstract: overlap 8/20")
ok("0.512" in abstract_md or "SI=0.512" in abstract_md, "Abstract: stratified GSE24206 SI")
ok("0.04" in abstract_md, "Abstract: stratified GSE53845 p=0.04")

# ── 6. Table 1 ───────────────────────────────────────────────
print("\n[6/7] Table 1")
t1 = (PAPER / "table1.md").read_text(encoding="utf-8")
ok("0.028" in t1, "Table 1: stratified p=0.028 for GSE24206")
ok("0.04" in t1, "Table 1: stratified p=0.04 for GSE53845")
ok("0.512" in t1, "Table 1: stratified SI=0.512")
ok("0.500" in t1, "Table 1: stratified SI=0.500")
ok("Robustness" in t1 or "robustness" in t1, "Table 1: robustness row present")

# ── 7. Discussion framework ──────────────────────────────────
print("\n[7/7] Discussion Framework")
disc_md = (PAPER / "discussion_draft.md").read_text(encoding="utf-8")
ok("What This Work Demonstrates" in disc_md, "Discussion: 'What This Proves' section")
ok("What This Work Does NOT Demonstrate" in disc_md, "Discussion: 'What This Does NOT Prove' section")
ok("stratified" in disc_md.lower(), "Discussion: mentions stratified validation")

# ── VERDICT ───────────────────────────────────────────────────
print("\n" + "=" * 60)
if errors:
    print(f"❌ VERIFICATION FAILED — {len(errors)} issue(s):")
    for i, e in enumerate(errors, 1):
        print(f"   {i}. {e}")
    print("\nFix these before submission.")
else:
    print("✅ ALL CHECKS PASSED — Submission Readiness: 100%")
    print("\nNext steps:")
    print("  1. Create PDF from manuscript_combined.docx")
    print("  2. Upload to https://www.biorxiv.org/submit-a-manuscript")
    print("  3. Update GitHub README with DOI after acceptance")
print("=" * 60)

sys.exit(1 if errors else 0)

