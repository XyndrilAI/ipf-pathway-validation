# Methods

## Study Design and Data Sources

We analyzed two independent bulk RNA-seq cohorts of idiopathic pulmonary
fibrosis (IPF) patients and healthy controls from the Gene Expression
Omnibus (GEO): GSE24206 (n=17 subjects: 11 IPF, 6 control) and GSE53845
(n=48 subjects: 40 IPF, 8 control). GSE24206 included multi-lobe tissue
biopsies (~2.4 samples per subject); these were aggregated to
subject-level means prior to all downstream analyses to ensure
statistical independence and prevent data leakage during
cross-validation. GSE53845 had a 1:1 sample-to-subject ratio requiring
no aggregation.

## Pathway-Level Scoring

Gene expression data were transformed to pathway-level enrichment scores
using single-sample Gene Set Enrichment Analysis (ssGSEA) via the gseapy
package (v1.1.11) with the Hallmark gene set collection (MSigDB v2024.1,
n=50 pathways). Rank-based normalization was applied to all samples.

## Robustness Validation Framework

We defined the unit of statistical independence as subject_id and
implemented a four-phase validation framework to assess pathway-level
reproducibility.

### Phase 0: Donor Leakage Audit

We verified that each cohort had deterministically reconstructable
subject identifiers and that no subjects appeared in multiple condition
groups. Maximum samples per subject was confirmed to be <=1 after
aggregation, eliminating leakage risk in train-test splits.

### Phase 1: Baseline Pathway Ranking

For each pathway, we computed the mean difference in ssGSEA scores
between IPF and control groups (effect size = mean_IPF - mean_CTRL).
Statistical significance of each pathway's differential activity was
assessed via label-permutation tests (500 permutations). The top-20
pathways by absolute effect size were selected as the baseline signature.

### Phase 2: Random Gene Set Control

To verify that observed pathway-level separability was not attributable
to chance pathway selection, we computed a Separability Index (SI) for
the baseline top-20 pathways using a Mann-Whitney U-based AUC metric
(SI = mean |AUC - 0.5| across pathways). We then generated 200 random
pathway sets of equal size (K=20) from the full set of 50 Hallmark
pathways and computed SI for each. The baseline SI was required to
exceed the random mean SI by at least 0.05 (pre-specified margin).
Empirical p-values were computed as the fraction of random SI values
exceeding the baseline SI.

### Phase 3: Holdout Generalization

We performed 50 iterations of random subject-level train-test splits
(70% train / 30% test). For each split, pathway effects were computed
independently on training and test sets, and the top-20 pathways were
ranked by absolute effect. Holdout SI was defined as the Jaccard
similarity between training and test top-20 pathway sets. Significance
was assessed against a label-permuted null distribution (500
permutations). The pass criterion required both statistical significance
(p < 0.05) and meaningful effect size (Delta > 0.10 vs. null mean).

## Statistical Analysis

Empirical p-values were computed as the fraction of null permutations
with SI >= observed SI. Significance threshold: p < 0.05. Borderline
results (0.05 <= p < 0.10) with robust effect sizes (Delta > 0.10) were
documented as underpowered but biologically consistent. All analyses
were performed in Python 3.12.10 (pandas 3.0.1, numpy 2.4.2, scipy
1.17.1, gseapy 1.1.11). Complete analysis code and run instructions are
available in the accompanying RUNBOOK.md.

