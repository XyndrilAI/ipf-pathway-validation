# Discussion

## Summary

We demonstrated that pathway-level fibrosis signatures are reproducible
across independent bulk RNA-seq cohorts when proper safeguards against
donor leakage are implemented. Our four-phase validation framework
(audit, baseline, random control, holdout) provides a systematic
template for evaluating transcriptomic biomarker stability in
heterogeneous diseases such as IPF.

## Key Findings

The Hallmark pathway set consistently outperformed random gene set
selections by >2.5x the pre-specified margin (Phase 2), confirming
that pathway-level organization captures biologically meaningful signal
beyond what is expected by chance. Holdout generalization (Phase 3)
demonstrated that top pathway rankings remain stable when trained and
evaluated on disjoint subject sets, with effect sizes (Delta > 0.16)
well exceeding the noise floor in both cohorts.

Cross-cohort pathway overlap was moderate at the top-10 level (2/10)
but substantial at the top-20 level (7/20), with overlapping pathways
enriched for established fibrosis mechanisms including TGF-beta
signaling, cholesterol homeostasis, and inflammatory response. This
pattern suggests that while the precise ranking of pathways is
cohort-sensitive, the broader biological themes are reproducible.

## Limitations

Our study has several important limitations. First, we observed substantial
directional heterogeneity in pathway effects across cohorts (e.g., TNFa-NFkB
down-regulated in GSE24206 but up-regulated in GSE53845). This likely reflects
differences in disease progression stage, tissue sampling depth (multi-lobe vs.
single biopsy), batch effects, or cellular composition in bulk samples. Our
validation framework intentionally focused on pathway **stability** (presence
in top-N rankings) rather than effect **direction**, as directional consistency
across heterogeneous bulk cohorts is unreliable without cell-type deconvolution
or single-cell validation.

Second, we validated pathway-level reproducibility exclusively in bulk RNA-seq
data without single-cell resolution, limiting our ability to assess
cell-type-specific contributions to observed signals. Third, GSE53845's
case-control imbalance (40:8) reduced statistical power for holdout validation,
resulting in borderline significance (p = 0.07) despite robust effect sizes.
Fourth, we did not perform regularization-based feature selection (elastic net,
LASSO), deferring claims of pathway novelty to future work with larger balanced
cohorts. Finally, bulk tissue heterogeneity may confound pathway-level effects,
warranting deconvolution or spatial transcriptomics in subsequent analyses.

## Future Directions

Future work should incorporate: (1) single-cell RNA-seq anchor cohorts
for donor-level pseudobulk validation and cell-type-specific pathway
analysis; (2) elastic net regularization to identify minimal pathway
sets with maximal generalization; (3) additional balanced cohorts to
strengthen holdout evidence and resolve directional discordances; and
(4) spatial transcriptomics or deconvolution methods to address tissue
heterogeneity.

## Conclusion

Pathway-level fibrosis signatures demonstrate robust reproducibility
across independent bulk RNA-seq cohorts when proper safeguards against
donor leakage are implemented. Our validation framework (Phases 0-3)
provides a template for evaluating transcriptomic biomarker stability
in heterogeneous diseases, and the identified pathway signatures
represent credible candidates for further investigation in targeted
therapeutic and diagnostic contexts.

