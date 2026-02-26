# Leakage-Controlled Validation Services - One Pager

**What:** Independent validation framework with audit trail (Phase 0-3 protocol)  
**Evidence:** Validated on 2 IPF cohorts (65 subjects total). Manuscript submitted to bioRxiv (February 2026) - preprint link will be added once published.  
**GitHub:** https://github.com/XyndrilAI/ipf-pathway-validation

---

## Why Different

✅ **Audit trail:** Zero-leakage verified (sample→subject mapping documented)  
✅ **Negative controls:** Permutation null + random baseline (no cherry-picking)  
✅ **Deterministic:** One-command reproducibility (`run_all` → verification report)

**Prior art gap:** Most validations lack leakage audit + negative controls → inflated claims.

---

## Three Services (Success-Only Pricing)

### 1. Multi-Cohort Expansion
**For:** Publications, grant proposals  
**DoD:** ≥2 new cohorts, each achieves:
- Phase 0: zero leakage (audit table)
- Phase 1: baseline > null, p < 0.10
- Verification: all checks PASS

**Timeline:** 21 days | **Fee:** €2,500 (€0 if <2 cohorts meet DoD)

---

### 2. Lab Adoption
**For:** Biotech/pharma internal standard  
**DoD:** Framework operational in client environment:
- `run_all` completes without errors
- Generates audit tables + verification report
- Client team runs independently (post-training)

**Timeline:** 14-21 days | **Fee:** €4,500 (€0 if framework non-operational)

---

### 3. Custom Validation
**For:** Independent signature assessment  
**DoD:** Analysis completes (Phase 0-3 on client data):
- Pre-registered analysis plan (timestamped)
- Verification report PASS
- Interpretation + code delivered

**Timeline:** 10-14 days | **Fee:** €2,000-€3,000 (€0 if analysis cannot complete)

**Note:** Payment for completion, NOT for positive results. Negative findings reported honestly.

---

## Success Criteria Details

See `APPENDIX_SUCCESS_CRITERIA.md` for:
- Numerical thresholds (p-values, effect sizes, Jaccard indices)
- Fail vs Stop vs Success definitions
- Client responsibilities
- Stop conditions (data quality, scope limits)

---

## Contact

Tony Keltakangas | fusion@xyndril.dev  
Software Developer / Independent Researcher | Fusion Dev Group, Finland  
GitHub: https://github.com/XyndrilAI/ipf-pathway-validation
