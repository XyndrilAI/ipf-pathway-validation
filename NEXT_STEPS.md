# Future Directions (Fundable Extensions)

## Current Status (PATH B Validated)

✅ **Achieved:**
- Leakage-controlled reproducibility protocol (Phase 0–3)
- 2 independent bulk RNA-seq cohorts (GSE24206, GSE53845)
- Subject-level independence verified (zero leakage)
- Baseline >> permutation null + random controls
- Holdout generalization demonstrated (1 significant, 1 borderline)
- Directional heterogeneity documented and discussed

⚠️ **Known Limitations:**
- Bulk-only (no scRNA validation)
- Fixed TOP_N = 20 (no sensitivity analysis)
- 2 cohorts (limited meta-analysis power)
- No clinical translation

---

## Extension 1: Robustness Grid (Parameter Sensitivity)

**Research Question:**
Do conclusions hold across reasonable parameter variations?

**Approach:**
- Test TOP_N ∈ {10, 20, 50}
- Multiple random seeds (5–10)
- Alternative scoring methods (GSVA vs ssGSEA)
- Permutation counts (100, 500, 1000)

**Deliverables:**
- Supplementary robustness table
- Variance decomposition analysis
- Sensitivity heatmap (parameter × cohort)
- Updated manuscript: "Robustness Analysis" section

**Resources:**
- Time: 1–2 weeks
- Compute: Standard cluster (parallelizable)
- No new data required

---

## Extension 2: Additional Independent Cohorts

**Research Question:**
How does cross-cohort stability scale with more datasets?

**Approach:**
- Identify 2–3 additional IPF bulk cohorts (GEO/ArrayExpress)
- Run same Phase 0–3 protocol per cohort
- Meta-analysis: quantify stability vs heterogeneity

**Deliverables:**
- Cohort-by-cohort summary table
- Meta-forest plot (SI distributions)
- Heterogeneity decomposition (I² statistic)
- Identify where reproducibility breaks (and why)

**Resources:**
- Time: 2–6 weeks (depends on data wrangling)
- Per cohort: ~3–5 days preprocessing + gating
- Compute: Standard (parallelizable across cohorts)

---

## Extension 3: PATH A Upgrade (scRNA-seq Validation)

**Research Question:**
Is pathway stability preserved at cell-type resolution?

**Approach:**
- Add 1 scRNA-seq IPF cohort with donor metadata
- Donor-level pseudobulk per cell type (preserve independence)
- Validate pathway signals cell-type specifically
- Compare bulk vs cell-type-resolved stability

**Deliverables:**
- Cell-type pathway heatmap
- Donor-level pseudobulk validation
- Fibroblast-specific pathway overlap (main analysis)
- Updated manuscript: PATH A results section

**Resources:**
- Time: 1–2 months
- Requires: scRNA preprocessing pipeline (Scanpy/Seurat)
- Compute: Moderate (pseudobulk aggregation)

---

## Extension 4: Clinical Translation (Prospective Validation)

**Research Question:**
Do signatures generalize to prospective clinical samples?

**Approach:**
- Collaborate with clinical site (ethics approval required)
- Collect prospective IPF samples (diagnostic/prognostic use case)
- Test pathway signatures on fresh data
- Evaluate clinical utility (ROC, decision curves)

**Deliverables:**
- Prospective validation results
- Clinical utility analysis
- Regulatory-grade documentation (if aiming for clinical use)

**Resources:**
- Time: 6–12 months (ethics + patient recruitment)
- Requires: Clinical collaboration + IRB approval
- Cost: Variable (depends on sequencing costs)

---

## Estimated Timeline & Resources

| Extension | Time | FTE | Compute | External Dependency |
|-----------|------|-----|---------|---------------------|
| Robustness Grid | 1–2 weeks | 0.25 | Standard | None |
| +2–3 Cohorts | 2–6 weeks | 0.5 | Standard | Public data only |
| PATH A (scRNA) | 1–2 months | 1.0 | Moderate | Public scRNA data |
| Clinical | 6–12 months | Variable | Standard | Clinical site + IRB |

**To "full validation" (PATH A + robustness + 2 cohorts):**
**~3–4 months, 1 FTE, modest compute**

---

## Design Principles (Preserved Across Extensions)

All extensions maintain:
- ✅ **Strict leakage control** (subject/donor independence)
- ✅ **Falsifiability** (permutation null + audit trail)
- ✅ **Reproducibility** (one-command pipeline + public data)
- ✅ **Honest limitations reporting**

---

## Contact for Collaborations

Tony Keltakangas
fusion@xyndril.dev
https://github.com/XyndrilAI/ipf-pathway-validation

