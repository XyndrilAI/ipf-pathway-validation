# Cover Letter

Dear Editors,

We submit our manuscript, "Pathway-level IPF signatures demonstrate robust
reproducibility across independent bulk cohorts under strict leakage control,"
for consideration as a Methodology article.

## Scientific Context

Transcriptomic biomarker studies frequently suffer from inflated replication
signals due to subtle donor/subject leakage, pseudoreplication, or evaluation
designs that fail to test subject-level generalization. We address these issues
with a compact, fully reproducible validation pipeline that quantifies stability
at the pathway level.

## Key Contributions

Using two independent GEO cohorts (GSE24206: n=17 subjects; GSE53845: n=48
subjects), we demonstrate:

1. **Rigorous leakage control** (Phase 0 audit + subject-level aggregation)
2. **Robust baseline stability** (Phase 1 LOCO p<0.01 both cohorts)
3. **Signal exceeds random controls** (Phase 2: Δ>0.12, p<0.001)
4. **Holdout generalization** (Phase 3 stratified: p=0.028 and p=0.04)
5. **Parameter sensitivity validated** (TOP_N robustness grid)
6. **Transparent limitation reporting** (directional heterogeneity documented)

All validation scripts, environment specifications, and reproduction instructions
are publicly available at: https://github.com/XyndrilAI/ipf-pathway-validation

## Reproducibility Statement

We provide complete reproducibility artifacts (RUNBOOK.md, ENVIRONMENT.txt,
requirements.txt) enabling independent verification of all reported results.
A one-command pipeline (`run_all.ps1`) reproduces all manuscript-critical
numbers from raw public GEO data.

## Ethics and Originality

This work uses only publicly available, de-identified GEO datasets. The
manuscript is original and not under consideration elsewhere. The author
declares no competing interests.

## AI Assistance Disclosure

Pipeline development was assisted by AI tools (Claude 3.7 Sonnet, GitHub
Copilot) for code optimization and documentation, acknowledged in the
manuscript.

Thank you for your consideration. We look forward to your feedback.

Sincerely,

Tony Keltakangas
Software Developer / Independent Researcher
Fusion Dev Group, Finland
fusion@xyndril.dev

