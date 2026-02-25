# Pathway-Level IPF Signature Validation (PATH B)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
Reproducible pipeline for validating pathway-level idiopathic pulmonary fibrosis (IPF) signatures across independent bulk RNA-seq cohorts with rigorous donor/subject leakage control.
## Overview
This repository implements a four-phase validation framework to assess pathway-level reproducibility in transcriptomic signatures while controlling for common pitfalls (donor leakage, pseudoreplication, overfitting).
### Key Finding (PATH B)
Pathway-level IPF signatures demonstrate **robust reproducibility** across independent bulk cohorts when subject-level independence is strictly enforced:
- **Phase 1 (LOCO)**: Both cohorts significantly exceed permutation null (p < 0.01)
- **Phase 2 (Random control)**: Baseline exceeds random gene sets (delta > 0.12, p < 0.001)
- **Phase 3 (Holdout)**: Generalization confirmed (GSE24206: p=0.03; GSE53845: p=0.07, borderline due to case-control imbalance)
**Critical caveat**: Effect **directions** vary across cohorts (likely disease stage/sampling variability). Validation focuses on pathway **stability** (top-N presence), not direction.
## Datasets
Public GEO datasets:
- **GSE24206**: 17 IPF subjects (multi-lobe, aggregated to subject-level)
- **GSE53845**: 48 subjects (40 IPF, 8 Control)
## Installation
```bash
# Clone repository
git clone https://github.com/XyndrilAI/ipf-pathway-validation.git
cd ipf-pathway-validation
# Create virtual environment (Python 3.12 recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
```
## Quick Start
### Windows (PowerShell 7)
```powershell
cd scripts
pwsh -ExecutionPolicy Bypass -File .\run_gates_01.ps1
```
### Manual execution (cross-platform)
```bash
# Phase 0: Donor leakage audit
python scripts/phase_0_audit.py \
  --dataset "GSE24206" \
  --metadata data/GSE24206/metadata.csv \
  --mode bulk \
  --subject-col "subject_id" \
  --outdir results/01_audit/GSE24206
# Phase 1: LOCO baseline + permutation null
python scripts/phase_1_baseline.py \
  --dataset "GSE24206" \
  --metadata data/GSE24206/metadata.csv \
  --scores data/GSE24206/pathway_scores.csv \
  --unit-col "subject_id" \
  --top-n 20 \
  --n-perm 500 \
  --outdir results/02_baseline/GSE24206
# Phase 3: Holdout validation
python scripts/phase_3_holdout.py \
  --dataset "GSE24206" \
  --metadata data/GSE24206/metadata.csv \
  --scores data/GSE24206/pathway_scores.csv \
  --unit-col "subject_id" \
  --n-splits 50 \
  --n-perm 500 \
  --outdir results/03_holdout/GSE24206
# Generate figures
python scripts/make_figures.py
```
## Validation Framework
### Phase 0: Donor Leakage Audit
- Verify deterministic subject identifiers
- Check for sample-level leakage (max samples/subject)
- Aggregate multi-sample subjects if needed
### Phase 1: LOCO Baseline
- Leave-one-subject-out cross-validation
- Compute Jaccard similarity on top-20 pathways (by absolute effect)
- Compare to label-permuted null (500 permutations)
### Phase 2: Random Control (Supplementary)
- Generate matched random gene sets (n=200)
- Verify baseline exceeds random by >= 0.05
### Phase 3: Holdout Generalization
- Repeated random subject splits (70% train, 50 iterations)
- Compute holdout Jaccard SI vs. permutation null
## Repository Structure
```
ipf-pathway-validation/
  scripts/          # All validation scripts
  docs/             # RUNBOOK + environment spec
  paper/            # Manuscript sections + figures
  reproducibility/  # Summary artifacts
  data/             # (not included - use GEO accessions)
```
## Documentation
- **Full methodology**: `paper/methods_draft.md`
- **Reproducibility guide**: `docs/RUNBOOK.md`
- **Environment**: `docs/ENVIRONMENT.txt`
- **Gate summary**: `reproducibility/FINAL_SUMMARY.txt`
## Citation
If you use this pipeline, please cite:
```
Keltakangas, T. (2025). Pathway-level IPF signatures demonstrate robust
reproducibility across independent bulk cohorts under strict leakage
control. BMC Bioinformatics [PENDING].
```
## Acknowledgments
Pipeline development assisted by AI tools (Claude 3.7 Sonnet, GitHub Copilot) for code optimization and documentation.
## License
MIT License - see [LICENSE](LICENSE) file for details.
## Contact
**Tony Keltakangas**
Software Developer / Independent Researcher
Fusion Dev Group, Finland
fusion@xyndril.dev
---
**Note**: This repository implements PATH B validation (bulk-only, robust baseline). scRNA-seq validation (PATH A upgrade) is planned for future work.