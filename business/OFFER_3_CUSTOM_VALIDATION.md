# Success-Only Offer: Custom Leakage-Controlled Validation

**Offer Type:** Independent Validation Service  
**Target:** Researchers, Biotech, Consultants (ad-hoc validation needs)  
**Status:** Proven framework, adaptable to custom hypotheses

---

## The Service

### What I Validate

**Your hypothesis, your data, rigorously validated:**

You provide:
- A biological signal/signature you want to validate
- Your own data, OR a public dataset you specify
- Success criteria (what would constitute "validation")

I provide:
- Leakage-controlled validation (Phase 0-3 protocol)
- Audit trail (every step documented, reproducible)
- Honest results (positive OR negative findings reported)
- Verification report (automated checks, no cherry-picking)

---

## What Makes This Different

### Standard Validation (what others do):

❌ Random train/test split (leakage risk)  
❌ No audit trail (can't verify subject independence)  
❌ Selective reporting (only "good" results shown)  
❌ Parameter tuning until p < 0.05 (overfitting)

### Leakage-Controlled Validation (what I do):

✅ **Phase 0:** Subject-level leakage audit (documented)  
✅ **Phase 1:** LOCO cross-validation + permutation null  
✅ **Phase 2:** Random control baseline (selection bias check)  
✅ **Phase 3:** Stratified holdout (class imbalance correction)  
✅ **Negative results reported** (as valuable as positive)  
✅ **Pre-registered analysis plan** (no post-hoc tuning)

---

## Proven Track Record

**Validation framework validated on:**
- 2 independent IPF bulk RNA-seq cohorts (n=65 subjects)
- Pathway-level signatures (Hallmark gene sets)
- All statistical gates PASS (p < 0.05, stratified)
- Robustness confirmed (TOP_N sensitivity, bootstrap CI)
- GitHub: https://github.com/XyndrilAI/ipf-pathway-validation
- Manuscript: bioRxiv submission-ready

**Key result:**
- Framework detected directional heterogeneity across cohorts
- Negative finding (inconsistent effect direction) reported honestly
- Conclusion: pathway *stability* > pathway *direction* in heterogeneous disease

**This proves:** I report what the data shows, not what you want to hear.

---

## What I Will Deliver

### Scope

Validate **your signature** on **your dataset** using Phase 0-3 leakage-controlled protocol.

### Deliverables

**1. Pre-Registration Document**

Before analysis begins:
- Hypothesis clearly stated
- Success criteria defined (numerical thresholds)
- Analysis plan specified (which tests, which parameters)
- Locked before seeing results (timestamped)

**2. Phase 0: Leakage Audit**

- Sample→subject mapping table
- Leakage quantification (if any)
- Recommendation: proceed as-is, aggregate samples, or exclude subjects

**3. Phase 1: LOCO Validation**

- Leave-one-subject-out cross-validation
- Baseline performance (your metric: AUC, accuracy, SI, etc.)
- Permutation null distribution (500+ iterations)
- Empirical p-value

**4. Phase 2: Negative Control**

- Random signature baseline (matched to your signature size/type)
- Comparison: your signature vs random
- Effect size quantification (Δ)

**5. Phase 3: Holdout Generalization**

- Stratified train/test splits (if class imbalance)
- Holdout performance
- Bootstrap confidence intervals (1000 resamples)
- Empirical p-value vs permutation null

**6. Verification Report**

- Automated checks (data integrity, numerical consistency)
- Reproducibility verification (all results deterministic)
- PASS/FAIL summary

**7. Interpretation Document**

- Plain-language summary (what the results mean)
- Statistical interpretation (p-values, effect sizes, CIs)
- Limitations (what the analysis does NOT prove)
- Recommendations (next steps, if validated OR if not)

**8. Code + Data Package**

- All analysis scripts (Python, MIT license)
- Processed data files (if shareable)
- REPRODUCE.md (how to re-run analysis)
- Environment specification (exact versions)

---

## Success Criteria (Customizable)

### Standard Success Criteria (default)

**Analysis completes successfully:**
✅ Phase 0-3 gates execute without errors  
✅ Verification report PASS  
✅ Results reproducible (deterministic)

**Interpretation provided:**
✅ Clear statement of findings (validated OR not validated)  
✅ Statistical measures reported (p-values, effect sizes, CIs)  
✅ Limitations documented

### Custom Success Criteria (if validation confirms hypothesis)

**Example:**
✅ Baseline performance exceeds permutation null (p < 0.05)  
✅ Baseline exceeds random control (Δ > threshold)  
✅ Holdout generalization confirmed (p < 0.10)

**Important:** Success fee is for **completing the analysis**, not for **positive results**. Negative results (hypothesis not validated) are equally valuable and fully reported.

### Failure Condition (€0 payment)

❌ Data incompatible with protocol (unresolvable technical issues)  
❌ Analysis cannot complete (computational errors)  
❌ Verification FAIL (results not reproducible)

**Note:** "Hypothesis not validated" is NOT a failure condition. You pay for rigorous analysis, not for the answer you want.

---

## Timebox & Process

**Total Duration:** 10-14 days from data access

**Day 1:** Pre-registration document finalized  
**Day 3:** Phase 0 audit complete, proceed/adjust decision  
**Day 7:** Phase 1-2 complete  
**Day 10:** Phase 3 complete  
**Day 14:** Interpretation + code package delivered

**Rush option:** +50% fee for 7-day delivery (if feasible given data size)

---

## Pricing (Success-Only for Analysis Completion)

### Base Validation Fee

**Standard dataset (n < 100 subjects):** €2,000

**Large dataset (n ≥ 100 subjects):** €3,000

**Complex validation (multiple signatures/cohorts):** Custom quote

### What "Success" Means for Payment

**Payment triggered by:**
- Analysis completes (Phase 0-3) ✅
- Verification report PASS ✅
- Interpretation + code delivered ✅

**Payment NOT dependent on:**
- Whether hypothesis is validated (positive vs negative results)
- Whether p < 0.05 (statistical significance)
- Whether client is "happy" with findings

**Honest reporting guarantee:** I report what the data shows. If you want cherry-picked results, this service is not for you.

### Payment Terms

- 50% upon pre-registration + Phase 0 audit complete
- 50% upon final delivery + verification PASS
- Invoice net 14 days

**Failure refund:** If analysis cannot complete (technical issues), 50% deposit refunded.

---

## Use Cases

### 1. Pre-Publication Validation

**Scenario:** You have a signature in your paper draft, want independent validation before submission.

**Why this helps:**
- Reviewers can't claim "leakage" or "overfitting"
- Audit trail increases credibility
- Negative results allow honest limitation reporting

### 2. Grant Proposal Pilot Data

**Scenario:** You need preliminary validation for a grant application.

**Why this helps:**
- Rigorous pilot strengthens proposal
- Null results inform revised hypotheses
- Reproducibility artifacts available for supplement

### 3. Biomarker Due Diligence

**Scenario:** Biotech evaluating a licensed signature, wants independent assessment.

**Why this helps:**
- Unbiased validation (I have no stake in outcome)
- Audit trail for regulatory purposes
- Honest assessment of generalization limits

### 4. Failed Replication Investigation

**Scenario:** Published signature doesn't replicate in your data, want to know why.

**Why this helps:**
- Leakage audit may reveal original study issues
- Heterogeneity quantification explains discordance
- Informs decision to pursue vs abandon

---

## What I Don't Do

❌ **P-hacking:** I don't try parameters until p < 0.05  
❌ **Cherry-picking:** I don't hide negative results  
❌ **Overinterpretation:** I don't claim causality from correlation  
❌ **Guarantee positive results:** Science doesn't work that way

✅ **What I do:** Honest, rigorous, reproducible validation. If your hypothesis doesn't hold up, you deserve to know *before* you publish/invest, not after.

---

## Technical Notes

### Data Requirements

**Minimum:**
- Expression data (bulk RNA-seq, microarray, or similar)
- Metadata (sample_id, subject_id, condition/phenotype)
- ≥20 subjects total (≥10 per condition preferred)

**Your signature:**
- Gene list (pathway, gene set, or custom genes)
- OR scoring function (if complex signature)

**Flexible formats:** CSV, TSV, HDF5, Seurat objects, etc. (preprocessing included)

### Confidentiality

- Your data stays confidential (NDA available if needed)
- Results shared only with you (unless you choose to publish)
- Code provided under MIT license (you can modify/share)

---

## Frequently Asked Questions

**Q: What if the validation shows my signature doesn't work?**  
A: That's valuable information. Better to know now than after publication or investment. I help interpret *why* (leakage? heterogeneity? overfitting?) so you can refine your approach.

**Q: Can you "optimize" parameters to make it work?**  
A: No. Parameter choices are pre-registered. Post-hoc tuning defeats the purpose of validation.

**Q: What if I disagree with your interpretation?**  
A: Data + code are yours. You can re-analyze or get a second opinion. My interpretation is provided, not mandated.

**Q: Do you publish validation results without permission?**  
A: Never. Your data, your results, your decision to share.

**Q: Can this validate non-transcriptomic signatures?**  
A: Framework is adaptable. If you have tabular data (features × samples) + labels, likely feasible. Contact to discuss.

---

## Next Steps

**Interested?**
1. Email brief description of your signature + dataset
2. I assess feasibility (within 48h)
3. If feasible, pre-registration document drafted
4. You approve analysis plan
5. Kickoff (payment 1 triggered)

**Not sure yet?**
- Review public validation example: https://github.com/XyndrilAI/ipf-pathway-validation
- Contact with questions (no obligation)

---

## Contact

**Tony Keltakangas**  
Software Developer / Independent Researcher  
Fusion Dev Group, Finland  

📧 fusion@xyndril.dev  
🔗 https://github.com/XyndrilAI/ipf-pathway-validation  
📍 Based in Finland (UTC+2/+3)

---

**This is a success-based engagement for analysis completion. Payment is NOT contingent on validating your hypothesis (positive results). Honest, rigorous validation only.**

*Offer valid for 60 days from date of initial contact.*
