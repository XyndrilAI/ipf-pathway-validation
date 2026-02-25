# Reproducibility Runbook - PATH B Validation

## Prerequisites
- Python 3.12 + venv at `D:\ipf_sprint\.venv`
- PowerShell 7
- Input data:
  - `data/<dataset>/metadata.csv` (sample_id, subject_id, condition)
  - `data/<dataset>/pathway_scores.csv` (sample_id, pathway scores)

## One-button run (all phases)
```powershell
cd D:\ipf_sprint\scripts
& "C:\Program Files\PowerShell\7\pwsh.exe" -ExecutionPolicy Bypass -File .\run_gates_01.ps1
```

Or use the PyCharm Run Configuration: **Run > run_gates_01**

## Individual phases

### Phase 0: Donor Leakage Audit
```powershell
cd D:\ipf_sprint\scripts

python .\phase_0_audit.py `
  --dataset "GSE24206" `
  --metadata "..\data\GSE24206\metadata.csv" `
  --mode bulk `
  --subject-col "subject_id" `
  --outdir "..\results\01_audit\GSE24206"

python .\phase_0_audit.py `
  --dataset "GSE53845" `
  --metadata "..\data\GSE53845\metadata.csv" `
  --mode bulk `
  --subject-col "subject_id" `
  --outdir "..\results\01_audit\GSE53845"
```

### Phase 1: Baseline Top Pathways + Permutation
```powershell
python .\phase_1_baseline.py `
  --dataset "GSE24206" `
  --metadata "..\data\GSE24206\metadata.csv" `
  --scores "..\data\GSE24206\pathway_scores.csv" `
  --unit-col "subject_id" `
  --condition-col "condition" `
  --ipf-value "IPF" `
  --ctrl-value "CTRL" `
  --top-n 20 `
  --n-perm 500 `
  --outdir "..\results\02_baseline\GSE24206"

python .\phase_1_baseline.py `
  --dataset "GSE53845" `
  --metadata "..\data\GSE53845\metadata.csv" `
  --scores "..\data\GSE53845\pathway_scores.csv" `
  --unit-col "subject_id" `
  --condition-col "condition" `
  --ipf-value "IPF" `
  --ctrl-value "CTRL" `
  --top-n 20 `
  --n-perm 500 `
  --outdir "..\results\02_baseline\GSE53845"
```

### Phase 2: Matched Random Sanity Check
```powershell
python .\phase_2_matched_random.py `
  --dataset "GSE24206" `
  --metadata "..\data\GSE24206\metadata.csv" `
  --scores "..\data\GSE24206\pathway_scores.csv" `
  --baseline-pathways "..\results\02_baseline\GSE24206\baseline_top_pathways.csv" `
  --unit-col "subject_id" `
  --condition-col "condition" `
  --ipf-value "IPF" `
  --ctrl-value "CTRL" `
  --n-random 200 `
  --margin 0.05 `
  --seed 42 `
  --outdir "..\results\03_matched_random\GSE24206"

python .\phase_2_matched_random.py `
  --dataset "GSE53845" `
  --metadata "..\data\GSE53845\metadata.csv" `
  --scores "..\data\GSE53845\pathway_scores.csv" `
  --baseline-pathways "..\results\02_baseline\GSE53845\baseline_top_pathways.csv" `
  --unit-col "subject_id" `
  --condition-col "condition" `
  --ipf-value "IPF" `
  --ctrl-value "CTRL" `
  --n-random 200 `
  --margin 0.05 `
  --seed 42 `
  --outdir "..\results\03_matched_random\GSE53845"
```

### Phase 3: Holdout Generalization
```powershell
python .\phase_3_holdout.py `
  --dataset "GSE24206" `
  --metadata "..\data\GSE24206\metadata.csv" `
  --scores "..\data\GSE24206\pathway_scores.csv" `
  --unit-col "subject_id" `
  --condition-col "condition" `
  --ipf-value "IPF" `
  --ctrl-value "CTRL" `
  --top-n 20 `
  --n-splits 50 `
  --n-perm 500 `
  --train-frac 0.7 `
  --outdir "..\results\04_holdout\GSE24206"

python .\phase_3_holdout.py `
  --dataset "GSE53845" `
  --metadata "..\data\GSE53845\metadata.csv" `
  --scores "..\data\GSE53845\pathway_scores.csv" `
  --unit-col "subject_id" `
  --condition-col "condition" `
  --ipf-value "IPF" `
  --ctrl-value "CTRL" `
  --top-n 20 `
  --n-splits 50 `
  --n-perm 500 `
  --train-frac 0.7 `
  --outdir "..\results\04_holdout\GSE53845"
```

## Expected Outputs
- `results/01_audit/<dataset>/metadata_audit.csv`
- `results/01_audit/<dataset>/donor_leakage_audit.csv`
- `results/02_baseline/<dataset>/baseline_top_pathways.csv`
- `results/03_matched_random/<dataset>/matched_random_si.csv`
- `results/03_matched_random/<dataset>/random_si_distribution.csv`
- `results/04_holdout/<dataset>/holdout_si.csv`

## Generate Figures
```powershell
cd D:\ipf_sprint\scripts
python .\make_figures.py
```
Outputs: `results/figures/figure1_phase2_baseline_vs_random.png|pdf`, `results/figures/figure2_phase3_holdout.png|pdf`

