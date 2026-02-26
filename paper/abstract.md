# Abstract

**Background:** Transcriptomic signatures of idiopathic pulmonary fibrosis (IPF)
often suffer from donor leakage and overfitting, limiting reproducibility across
independent cohorts. Rigorous validation frameworks are needed to distinguish
robust pathway-level signals from technical artifacts.

**Methods:** We developed a four-phase validation framework to assess pathway-level
reproducibility in bulk RNA-seq data from two independent IPF cohorts (GSE24206:
n=17 subjects; GSE53845: n=48 subjects; 65 total). Subject-level independence was
enforced via leave-one-subject-out cross-validation and holdout generalization
testing. Pathway enrichment was quantified using single-sample gene set enrichment
analysis (ssGSEA) with Hallmark gene sets (n=50), and reproducibility measured via
Jaccard similarity of top-20 pathways ranked by absolute effect size.

**Results:** Phase 0 audit confirmed zero subject-level leakage (n=65 samples,
2 cohorts). Leave-one-subject-out validation (Phase 1) demonstrated significant
pathway separability (p<0.01 both cohorts). Baseline exceeded matched random
gene sets (Phase 2: Δ>0.12, p<0.001). Stratified holdout generalization (Phase 3)
confirmed reproducibility (GSE24206: SI=0.512, p=0.028; GSE53845: SI=0.500,
p=0.04). Robustness analysis validated TOP_N=20 as optimal (vs 10/50). Cross-cohort
overlap (8/20 pathways) revealed directional heterogeneity, indicating pathway
*stability* rather than *direction* is the appropriate reproducibility metric.

**Conclusions:** Pathway-level fibrosis signatures demonstrate robust reproducibility
when donor leakage is rigorously controlled, though effect directions vary across
heterogeneous bulk samples. Our validation framework provides a methodological
template for evaluating transcriptomic biomarker stability in complex diseases.

**Keywords:** idiopathic pulmonary fibrosis, pathway analysis, cross-validation,
reproducibility, bulk RNA-seq, donor leakage

