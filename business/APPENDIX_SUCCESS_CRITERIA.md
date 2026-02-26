# Appendix A: Success Criteria - Detailed Specifications

This document defines measurable, falsifiable success criteria for all three service offerings. These criteria eliminate interpretation ambiguity and enable clear success/failure determination.

---

## General Definitions

### Success Categories

**SUCCESS:** All primary criteria met → Full payment  
**PARTIAL SUCCESS:** Some criteria met → Negotiated partial payment (if applicable)  
**STOP:** Project halted due to valid technical/data reasons → No payment, no blame  
**FAIL:** Criteria not met due to provider error → No payment, provider liable

### Phase Definitions (Applies to All Services)

**Phase 0: Leakage Audit**
- Input: Metadata CSV (sample_id, subject_id, condition)
- Process: Identify duplicate subjects across splits
- Output: `leakage_audit.csv` with leakage count
- **PASS criteria:** leakage_count = 0 OR documented aggregation strategy

**Phase 1: LOCO Baseline vs Null**
- Input: Expression data + metadata
- Process: Leave-one-subject-out CV + permutation null (≥500 iterations)
- Output: `baseline_si_loco.csv`, `baseline_null.csv` 
- **PASS criteria:** 
  - baseline_si_mean computed (no NaN)
  - empirical_p < 0.10 (default threshold, customizable)

**Phase 2: Random Control**
- Input: Same as Phase 1
- Process: Generate ≥100 matched random gene sets, compare baseline
- Output: `baseline_vs_random.csv` 
- **PASS criteria:**
  - Δ = baseline_si_mean - random_si_mean > 0.05 (effect size threshold)
  - empirical_p < 0.05

**Phase 3: Holdout Generalization**
- Input: Same as Phase 1
- Process: Stratified holdout (70/30 split, ≥50 iterations) + permutation null
- Output: `holdout_si.csv` 
- **PASS criteria:**
  - holdout_si_mean ≥ 0.40 (Jaccard index threshold, customizable)
  - empirical_p < 0.10 (default, customizable)
  - Bootstrap 95% CI does not include 0

**Verification Report**
- Input: All Phase 0-3 outputs
- Process: Run `verify_manuscript.py` or equivalent
- Output: `verification_report.txt` 
- **PASS criteria:** All critical checks return PASS status

---

## Service 1: Multi-Cohort Expansion

### Primary Success Criteria (ALL must be met)

1. **≥2 new cohorts complete Phase 0-3**
   - Each cohort processes without fatal errors
   - Each cohort generates all required output files

2. **Each cohort Phase 0 PASS**
   - leakage_count = 0 OR documented aggregation
   - Audit table generated (no missing subjects)

3. **≥2 cohorts Phase 1 PASS**
   - empirical_p < 0.10 (permutation test)
   - baseline_si_mean - null_si_mean > 0 (positive effect)

4. **Verification PASS**
   - All automated checks pass for all cohorts
   - No data integrity errors

### Secondary Success Criteria (≥1 for full payment)

5. **Strong statistical evidence**
   - ≥2 cohorts: Phase 3 holdout p < 0.05 AND SI ≥ 0.45

6. **Cross-cohort consistency**
   - Median pairwise Jaccard overlap ≥ 6/20 pathways

### Stop Conditions (Valid, No Payment, No Blame)

- **Insufficient GEO data:** If <2 suitable cohorts exist in GEO (after reasonable search)
- **Annotation errors:** Dataset metadata fundamentally incompatible (no subject IDs recoverable)
- **Sample size:** Cohort has <10 subjects per condition (insufficient for holdout)

### Client Responsibilities

- Approve cohort selection (if specific preferences)
- Define custom thresholds (if default not acceptable)

---

## Service 2: Lab Adoption

### Primary Success Criteria (ALL must be met)

1. **Framework installed**
   - All dependencies installed (requirements.txt)
   - `run_all` script executes without fatal errors
   - Output files generated in expected locations

2. **Test dataset validation PASS**
   - Phase 0-3 complete on 1 test dataset (client choice or demo)
   - Verification report PASS
   - Audit trail generated

3. **Documentation complete**
   - Installation guide tested (client team can follow)
   - Usage manual enables independent operation

### Secondary Success Criteria (≥1 for full payment)

4. **Independent operation**
   - Client team runs pipeline on 2nd dataset without provider assistance
   - Verification PASS on independent run

5. **Workflow integration**
   - Data import automated (from client's storage)
   - Output export to client's preferred format

### Stop Conditions (Valid)

- **Environment incompatibility:** Client infrastructure fundamentally incompatible (e.g., no Python support, firewall blocks dependencies)
- **Data format irreconcilable:** Client data structure requires >5 days preprocessing work (out of scope)

### Client Responsibilities

- Provide environment access (SSH, credentials, or VM)
- Designate 1 technical contact (respond within 48h)
- Provide test dataset (or approve demo dataset)

---

## Service 3: Custom Validation

### Primary Success Criteria (ALL must be met)

1. **Pre-registration complete**
   - Hypothesis stated clearly
   - Analysis plan documented (timestamped before data access)
   - Success thresholds agreed upon

2. **Phase 0-3 execution**
   - All phases complete without fatal errors
   - Output files generated

3. **Verification PASS**
   - Automated checks pass
   - Results reproducible (deterministic)

4. **Deliverables complete**
   - Interpretation document (findings + limitations)
   - Code + data package (if shareable)

### Secondary Success Criteria (NOT required for payment)

- Hypothesis validated (positive results)
- Statistical significance achieved (p < 0.05)

**CRITICAL:** Payment is for analysis completion, NOT for positive results. Negative findings are equally valuable and fully reported.

### Stop Conditions (Valid)

- **Data incompatibility:** Data structure fundamentally incompatible with protocol (e.g., no expression matrix recoverable)
- **Signature undefined:** Client cannot provide clear signature definition (gene list or scoring function)
- **Computational limits:** Dataset size exceeds reasonable computational capacity (>10,000 subjects without cluster access)

### Client Responsibilities

- Provide data + metadata (or specify public dataset)
- Define signature (gene list or scoring function)
- Approve pre-registration document
- Define custom thresholds (if defaults not acceptable)

---

## Numerical Thresholds (Default Values)

| Metric | Default Threshold | Customizable? | Rationale |
|--------|-------------------|---------------|-----------|
| Phase 0 leakage | 0 | No | Zero tolerance for leakage |
| Phase 1 empirical p | < 0.10 | Yes | Permutation test significance |
| Phase 2 Δ (effect size) | > 0.05 | Yes | Baseline vs random difference |
| Phase 2 empirical p | < 0.05 | Yes | Random control significance |
| Phase 3 SI (Jaccard) | ≥ 0.40 | Yes | Holdout overlap threshold |
| Phase 3 empirical p | < 0.10 | Yes | Holdout significance |
| Bootstrap CI | Does not include 0 | No | Effect stability |

**Customization:** Thresholds can be adjusted in pre-registration (before analysis). Post-hoc changes not permitted.

---

## Fail vs Stop vs Success - Decision Tree
```
Data received
│
├─ Data incompatible (no expression matrix) → STOP (€0, no blame)
├─ Metadata missing (no subject IDs) → STOP (€0, no blame)
│
└─ Data processable
   │
   ├─ Phase 0-3 executes, verification PASS → SUCCESS (€€€)
   ├─ Phase 0-3 executes, verification FAIL (provider error) → FAIL (€0, provider liable)
   ├─ Phase 0-3 executes, criteria not met (e.g., p > threshold) → SUCCESS (€€€, honest negative result)
   │
   └─ Phase 0-3 cannot execute (fatal errors) → Investigate
      │
      ├─ Provider code bug → FAIL (€0, provider liable, fix + rerun)
      └─ Data quality issue (e.g., all NaNs) → STOP (€0, no blame)
```

---

## Payment Trigger Checklist

**Before invoicing, verify:**
- [ ] All primary success criteria met (per service definition above)
- [ ] ≥1 secondary criterion met (if applicable)
- [ ] Client confirms receipt of all deliverables
- [ ] No unresolved disputes over success determination

**If any unchecked:** Do not invoice. Resolve or classify as STOP/FAIL.

---

## Dispute Resolution

**If disagreement on success/failure:**
1. Review pre-registration document (what was agreed?)
2. Check verification report (objective pass/fail)
3. Independent code review (GitHub public, external verification possible)

**Binding:** Verification report PASS/FAIL status is final arbiter (automated, no human interpretation).

---

## Updates to Criteria

This appendix may be updated for:
- New service types
- Improved verification checks
- Client-requested custom thresholds

**Version control:** All changes tracked in Git, timestamped.

**Current version:** 1.0 (Feb 2025)

---

## Contact for Questions

Tony Keltakangas | fusion@xyndril.dev  
All criteria public: https://github.com/XyndrilAI/ipf-pathway-validation/tree/main/business
