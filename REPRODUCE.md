# One-Command Reproducibility

This repository enables **falsifiable, one-command reproduction** of all manuscript-critical results.

## Quick Start (TL;DR)

```powershell
# Windows (PowerShell 7)
git clone https://github.com/XyndrilAI/ipf-pathway-validation.git
cd ipf-pathway-validation
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Download data (see Data Preparation below)

# Run full pipeline (ONE COMMAND)
pwsh -ExecutionPolicy Bypass -File scripts\run_all.ps1
```

## System Requirements

- **Python:** 3.12+ (tested on 3.12.10)
- **OS:** Windows 10/11 (PowerShell 7), Linux, or macOS
- **Dependencies:** See `requirements.txt`
- **Compute:** Standard laptop (no GPU required)
- **Runtime:** ~10–30 minutes depending on CPU (permutations = 500)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/XyndrilAI/ipf-pathway-validation.git
cd ipf-pathway-validation
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Data Preparation

This project uses **public GEO datasets**:

| Dataset | Subjects | Design | GEO Link |
|---------|----------|--------|----------|
| GSE24206 | 17 (11 IPF, 6 CTRL) | Multi-lobe bulk RNA-seq (aggregated to subject mean) | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24206) |
| GSE53845 | 48 (40 IPF, 8 CTRL) | 1:1 bulk RNA-seq | [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE53845) |

### Required Input Files

Place data files in the following structure:

```
data/
  GSE24206/
    metadata.csv          # sample_id, condition, subject_id
    pathway_scores.csv    # sample_id + 50 Hallmark pathway columns
  GSE53845/
    metadata.csv
    pathway_scores.csv
```

**`metadata.csv` format:**
```csv
sample_id,condition,subject_id
CTRL_A,CTRL,CTRL_A
IPF_140,IPF,IPF_140
...
```

**`pathway_scores.csv`:** Generated via ssGSEA (Hallmark v2024.1, rank normalization).
See `docs/RUNBOOK.md` for the full pathway scoring procedure using `scripts/make_bulk_pathway_scores.py`.

## Running the Pipeline

### Full Pipeline (One Command)

**Windows (PowerShell 7):**
```powershell
pwsh -ExecutionPolicy Bypass -File scripts\run_all.ps1
```

**Linux/macOS (PowerShell Core):**
```bash
pwsh -File scripts/run_all.ps1
```

### What Gets Executed

The pipeline runs **6 steps** in order:

| Step | Phase | Description |
|------|-------|-------------|
| 1/6 | Phase 0 | Donor leakage audit (subject independence check) |
| 2/6 | Phase 1 | Baseline pathway ranking + permutation null (500 perms) |
| 3/6 | Phase 2 | Random gene set control (200 random sets, margin ≥ 0.05) |
| 4/6 | Phase 3 | Holdout generalization (50 splits × 500 perms) |
| 5/6 | Figures | Generate publication-ready PDFs |
| 6/6 | Verify | Cross-check manuscript numbers against CSV outputs |

### Individual Phase Execution

You can also run phases individually. See `docs/RUNBOOK.md` or `scripts/run_gates_01.ps1` for per-dataset commands.

## Expected Outputs

After a successful run:

```
results/
  01_audit/
    GSE24206/donor_leakage_audit.csv, metadata_audit.csv
    GSE53845/donor_leakage_audit.csv, metadata_audit.csv
  02_baseline/
    GSE24206/baseline_top_pathways.csv
    GSE53845/baseline_top_pathways.csv
  03_matched_random/
    GSE24206/matched_random_si.csv, random_si_distribution.csv
    GSE53845/matched_random_si.csv, random_si_distribution.csv
  04_holdout/
    GSE24206/holdout_si.csv
    GSE53845/holdout_si.csv
  figures/
    figure1_phase2_baseline_vs_random.pdf
    figure2_phase3_holdout.pdf
  verification_report.txt
```

## Verification

**Critical manuscript numbers** (must match after reproduction):

| Metric | GSE24206 | GSE53845 |
|--------|----------|----------|
| Phase 1: Top-20 max perm p | 0.028 | 0.022 |
| Phase 2: Baseline SI | 0.381 | 0.349 |
| Phase 2: Δ (vs random) | 0.156 | 0.128 |
| Phase 3: Holdout SI | 0.499 ± 0.136 | 0.467 ± 0.139 |
| Phase 3: p-value | 0.03 | 0.07 |
| Phase 0: Leakage | 0 subjects | 0 subjects |

**Automated check:**
```bash
cat results/verification_report.txt
# Expected final line: VERDICT: ✅ PASS — All checks passed.
```

**If numbers do not match**, open an issue with:
- OS + Python version
- Full `verification_report.txt`
- Git commit hash: `git rev-parse HEAD`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Missing data files | Ensure `data/*/metadata.csv` and `data/*/pathway_scores.csv` exist (see Data Preparation) |
| Module not found | Verify venv is activated; re-run `pip install -r requirements.txt` |
| Permission errors (Windows) | Run: `Set-ExecutionPolicy -Scope CurrentUser Bypass` |
| PowerShell 7 not found | Install from https://github.com/PowerShell/PowerShell/releases |
| Verification FAIL | Compare your `verification_report.txt` line-by-line; check numpy/pandas versions |

## Citation

```
Keltakangas, T. (2025). Pathway-level IPF signatures demonstrate robust
reproducibility across independent bulk cohorts under strict leakage
control. [Journal/Preprint TBD].
```

## License

MIT License — see `LICENSE` file.

## Contact

**Tony Keltakangas**
Software Developer / Independent Researcher
Fusion Dev Group, Finland
fusion@xyndril.dev

