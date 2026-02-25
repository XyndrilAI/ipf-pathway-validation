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

**Results:** Both cohorts significantly exceeded permutation null baselines
(Phase 1 LOCO: p < 0.01 for both) and random pathway controls (Phase 2:
Delta > 0.12, p < 0.001). Holdout validation demonstrated generalization to
independent subjects (GSE24206: SI = 0.50 +/- 0.14, p = 0.03; GSE53845:
SI = 0.47 +/- 0.14, p = 0.07 with documented case-control imbalance).
Top-20 pathways showed partial cross-cohort overlap (7/20 pathways) including
cholesterol homeostasis, TNFa-NFkB signaling, and matrix remodeling, despite
substantial directional heterogeneity attributable to disease stage and tissue
sampling variability.

**Conclusions:** Pathway-level fibrosis signatures demonstrate robust reproducibility
when donor leakage is rigorously controlled, though effect directions vary across
heterogeneous bulk samples. Our validation framework provides a methodological
template for evaluating transcriptomic biomarker stability in complex diseases.

**Keywords:** idiopathic pulmonary fibrosis, pathway analysis, cross-validation,
reproducibility, bulk RNA-seq, donor leakage

