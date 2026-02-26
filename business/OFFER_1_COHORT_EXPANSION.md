# Success-Only Offer: Multi-Cohort IPF Pathway Validation

**Offer Type:** Cohort Expansion  
**Target:** Academic PIs, Grant Proposals, Publications  
**Status:** PATH B pilot complete (2 cohorts, all gates PASS)

---

## What Exists Now (Proven Pilot)

**PATH B Validation Framework** - fully implemented and verified:

✅ **Phase 0-3 leakage-controlled protocol**
- Zero donor leakage (audit trail: 65 samples, 2 cohorts)
- LOCO cross-validation (p < 0.01 both cohorts)
- Random control baseline (Δ > 0.12, p < 0.001)
- Stratified holdout (p < 0.05 both cohorts)

✅ **Robustness validated**
- TOP_N sensitivity analysis (10/20/50)
- Stable across 5 independent seeds
- Bootstrap confidence intervals

✅ **Deterministic reproducibility**
- One-command pipeline: `pwsh scripts/run_all.ps1` 
- Automated verification (32 checks)
- GitHub: https://github.com/XyndrilAI/ipf-pathway-validation

✅ **Published Evidence (pending)**
- Manuscript submitted to bioRxiv (February 2026)
- Preprint DOI will be available within 24-48 hours
- Full reproducibility: https://github.com/XyndrilAI/ipf-pathway-validation

---

## What I Will Deliver (Success-Only Extension)

### Scope

Extend PATH B validation to **2-3 additional independent IPF bulk RNA-seq cohorts** from GEO, using identical Phase 0-3 protocol.

### Deliverables

**1. Per-Cohort Validation Artifacts**

For each new cohort:
- Leakage audit table (sample→subject mapping, zero leakage verified)
- Phase 1: LOCO baseline SI + permutation null (500 iterations)
- Phase 2: Random control comparison (100 matched gene sets)
- Phase 3: Stratified holdout SI + bootstrap CI (1000 resamples)
- Automated verification report (all checks documented)

**2. Meta-Analysis Outputs**

- `cohort_summary_table.csv`: All cohorts (original + new), all gates
  - Columns: dataset, n_subjects, SI_mean, SI_std, empirical_p, gate_status
- Cross-cohort heterogeneity heatmap (pathway overlap visualization)
- Overlap analysis: Jaccard similarity matrix (all pairwise cohort comparisons)
- Effect direction concordance table (pathway-level heterogeneity)

**3. Updated Manuscript Sections**

- Methods: Multi-cohort validation description
- Results: Cohort-by-cohort summary table + heterogeneity quantification
- Discussion: Interpretation of cross-cohort variance + generalization limits
- Supplementary Table S6: Complete multi-cohort summary

**4. Reproducibility Guarantee**

- All new cohorts integrated into `run_all.ps1` pipeline
- Verification script extended (validates all cohorts)
- GitHub repository updated (all data processing scripts)
- REPRODUCE.md updated with new cohort instructions

---

## Success Criteria (Measurable & Falsifiable)

### Primary Criteria (ALL must pass for payment)

✅ **≥2 new cohorts complete Phase 0-3 gates**
- Each cohort: Phase 0 audit shows zero leakage
- Each cohort: Phase 1 baseline SI computed + permutation null
- Each cohort: Phase 3 holdout generalization tested

✅ **Baseline exceeds null for ≥2 new cohorts**
- Empirical p < 0.10 (permutation test, 500 iterations)
- Effect size Δ > 0 (baseline SI - null SI)

✅ **Verification report PASS**
- Automated checks pass for all cohorts
- All CSV files validate (no missing data, correct schema)
- Figures render correctly (no errors)

### Secondary Criteria (≥1 must pass for full payment)

✅ **Strong statistical significance in ≥2 new cohorts**
- Stratified holdout SI ≥ 0.45 AND empirical p < 0.05

✅ **Cross-cohort consistency maintained**
- Median cross-cohort overlap ≥ 6/20 pathways (Jaccard on top-20)

### Failure Condition (€0 payment)

❌ If <2 new cohorts complete Phase 0-3 gates  
❌ If verification report FAIL (automated checks)  
❌ If data processing errors prevent reproducibility

---

## Timebox & Milestones

**Total Duration:** 21 calendar days from data access

**Milestones:**
- **Day 3:** Data download + preprocessing complete (1st cohort)
- **Day 7:** 1st cohort Phase 0-3 complete, verification PASS
- **Day 14:** 2nd cohort complete + meta-analysis started
- **Day 21:** All deliverables complete, final verification PASS

**Early completion:** If all success criteria met before Day 21, deliverables provided immediately (no delay).

**Progress updates:** Every 7 days (brief status email)

---

## Pricing (Success-Only)

### Success Fee Structure

**Base success fee:** €2,500

**Payment triggered by:**
- All Primary success criteria met ✅
- ≥1 Secondary criterion met ✅
- All deliverables provided + verification PASS ✅

**Failure scenario:** €0 payment
- If success criteria not met, no payment obligation
- Client retains all intermediate work products (partial results)

**Payment terms:**
- Invoice upon delivery of final verification report
- Payment within 14 days of client confirmation
- Wire transfer or PayPal (client preference)

---

## Why This Matters for Your Work

### For Grant Proposals

✅ **"Multi-cohort validation (n=4-5 independent datasets)"** is significantly stronger than "2 cohorts"  
✅ Heterogeneity quantification demonstrates methodological rigor  
✅ Audit trail enables reproducibility claims in grant text  
✅ Negative results (if any) are equally valuable (shows boundaries)

### For Publications

✅ Reviewer-proof methodology (all standard objections pre-addressed)  
✅ Meta-analysis framework (cohort-level variance quantified)  
✅ Transparent limitations (directional heterogeneity documented)  
✅ Supplementary materials complete (all data available)

### For Future Research

✅ Established protocol portable to other diseases  
✅ Standardized leakage control framework (generalizable)  
✅ Baseline for PATH A upgrade (scRNA validation)

---

## Technical Notes

### Data Requirements (from client)

**NOT required:** Client does not need to provide data  
**Handled by me:** GEO dataset selection + download + preprocessing

**Client input (optional):**
- Preferred GEO accessions (if specific cohorts desired)
- Exclusion criteria (e.g., avoid overlapping patient cohorts)

### Computational Environment

- All processing on my infrastructure (no client compute needed)
- Results delivered as CSV + PDF (platform-agnostic)
- Source code available on GitHub (MIT license)

### Assumptions & Risks

**Assumptions:**
- GEO datasets are accessible and well-annotated
- Sufficient IPF vs Control samples per cohort (≥10 per group)
- Pathway scoring (ssGSEA) feasible from available data

**Risk mitigation:**
- If dataset proves unusable (annotation errors, insufficient samples), replacement cohort selected at no additional timeline cost
- Client notified immediately if data quality issues arise

---

## Next Steps

**Interested?** Contact to discuss:
- Specific cohort preferences (if any)
- Timeline alignment with grant/publication deadlines
- Success criteria customization (if needed)

**Not ready yet?** Review PATH B pilot results:
- GitHub: https://github.com/XyndrilAI/ipf-pathway-validation
- Preprint: [bioRxiv link when available]

---

## Contact

**Tony Keltakangas**  
Software Developer / Independent Researcher  
Fusion Dev Group, Finland  

📧 fusion@xyndril.dev  
🔗 https://github.com/XyndrilAI/ipf-pathway-validation  
📍 Based in Finland (UTC+2/+3)

---

**This is a success-based engagement. No payment unless success criteria are met.**

*Offer valid for 60 days from date of initial contact.*
