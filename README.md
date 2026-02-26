# Pathway-Level IPF Signature Validation (PATH B)

[![Preprint](https://img.shields.io/badge/preprint-bioRxiv-blue)](https://www.biorxiv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

> **Status:** Manuscript complete. Submission to bioRxiv pending (Feb 2026).

Reproducible pipeline for validating pathway-level idiopathic pulmonary fibrosis (IPF) signatures across independent bulk RNA-seq cohorts with rigorous donor/subject leakage control.

## Overview

This repository implements a four-phase validation framework to assess pathway-level reproducibility in transcriptomic signatures while controlling for common pitfalls (donor leakage, pseudoreplication, overfitting).

### Key Finding (PATH B)

Pathway-level IPF signatures demonstrate **robust reproducibility** across independent bulk cohorts when subject-level independence is strictly enforced:
- **Phase 1 (LOCO)**: Both cohorts significantly exceed permutation null (p < 0.01)
- **Phase 2 (Random control)**: Baseline exceeds random gene sets (Δ > 0.12, p < 0.001)
- **Phase 3 (Stratified holdout)**: Generalization confirmed (GSE24206: SI=0.512, p=0.028; GSE53845: SI=0.500, p=0.04)
- **Robustness**: TOP_N=20 validated as optimal across sensitivity grid

**Critical caveat**: Effect **directions** vary across cohorts (likely disease stage/sampling variability). Validation focuses on pathway **stability** (top-N presence), not direction.

## 💼 Commercial Services

Looking for leakage-controlled validation for your research?

- **Multi-Cohort Expansion:** Extend validation to additional datasets
- **Lab Adoption:** Deploy framework in your environment
- **Custom Validation:** Independent assessment of your signatures

See [business offers](business/) for details. **Success-only pricing** (no payment unless criteria met).

## Preprint & Reproducibility

**Preprint:** [bioRxiv DOI — Coming Soon]
**One-command reproduction:** See [REPRODUCE.md](REPRODUCE.md)
**Future work & funding roadmap:** See [NEXT_STEPS.md](NEXT_STEPS.md)

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

### One-Command Pipeline (Recommended)
```powershell
# Windows (PowerShell 7)
pwsh -ExecutionPolicy Bypass -File scripts\run_all.ps1
```

This runs all 6 steps: Phase 0 audit -> Phase 1 baseline -> Phase 2 random control -> Phase 3 holdout -> Figures -> Verification.

### Per-Phase Execution
```powershell
# Or run the gate-based runner (same phases, alternative script)
pwsh -ExecutionPolicy Bypass -File scripts\run_gates_01.ps1
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
    run_all.ps1     # One-command full pipeline
    run_gates_01.ps1 # Gate-based runner
    phase_0_audit.py
    phase_1_baseline.py
    phase_2_matched_random.py
    phase_3_holdout.py
    make_figures.py
    verify_manuscript.py
  docs/             # RUNBOOK + environment spec
  paper/            # Manuscript sections + figures
  reproducibility/  # Summary artifacts
  data/             # (not included - use GEO accessions)
  REPRODUCE.md      # One-command reproduction guide
  NEXT_STEPS.md     # Fundable extension roadmap
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