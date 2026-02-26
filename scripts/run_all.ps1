# scripts/run_all.ps1
# Full reproducibility pipeline: Phase 0-3 + figures + verification
# Usage: pwsh -ExecutionPolicy Bypass -File scripts\run_all.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Assert-File($path) {
    if (-not (Test-Path $path)) {
        throw "Missing required file: $path"
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "IPF Pathway Validation - Full Pipeline"  -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Started:  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "PowerShell: $($PSVersionTable.PSVersion)"

# ── Resolve paths robustly ──────────────────────────────────
$root    = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$scripts = (Resolve-Path $PSScriptRoot).Path
$dataDir = Join-Path $root "data"
$resDir  = Join-Path $root "results"

Set-Location $root
Write-Host "Project root: $root"

# ── Create output directories ───────────────────────────────
Write-Host "`nCreating output directories..." -ForegroundColor Yellow
foreach ($d in @(
    "results/01_audit/GSE24206",  "results/01_audit/GSE53845",
    "results/02_baseline/GSE24206", "results/02_baseline/GSE53845",
    "results/03_matched_random/GSE24206", "results/03_matched_random/GSE53845",
    "results/04_holdout/GSE24206", "results/04_holdout/GSE53845",
    "results/figures", "results/paper"
)) {
    New-Item -ItemType Directory -Force -Path (Join-Path $root $d) | Out-Null
}

# ── Dataset definitions ─────────────────────────────────────
$datasets = @(
    @{ name="GSE24206"; unit="subject_id" },
    @{ name="GSE53845"; unit="subject_id" }
)

# ═════════════════════════════════════════════════════════════
# [1/6] Phase 0: Donor Leakage Audit
# ═════════════════════════════════════════════════════════════
Write-Host "`n[1/6] Phase 0: Donor Leakage Audit" -ForegroundColor Green
Assert-File (Join-Path $scripts "phase_0_audit.py")

foreach ($ds in $datasets) {
    $meta = Join-Path $dataDir "$($ds.name)/metadata.csv"
    Assert-File $meta

    & python (Join-Path $scripts "phase_0_audit.py") `
        --dataset $ds.name `
        --metadata $meta `
        --mode bulk `
        --subject-col $ds.unit `
        --outdir (Join-Path $resDir "01_audit/$($ds.name)")
}

# ═════════════════════════════════════════════════════════════
# [2/6] Phase 1: Baseline Pathway Ranking + Permutation Null
# ═════════════════════════════════════════════════════════════
Write-Host "`n[2/6] Phase 1: Baseline Pathway Ranking" -ForegroundColor Green
Assert-File (Join-Path $scripts "phase_1_baseline.py")

foreach ($ds in $datasets) {
    $meta   = Join-Path $dataDir "$($ds.name)/metadata.csv"
    $scores = Join-Path $dataDir "$($ds.name)/pathway_scores.csv"

    if (-not (Test-Path $scores)) {
        Write-Host "  SKIP Phase 1 ($($ds.name)): pathway_scores.csv missing" -ForegroundColor Yellow
        continue
    }

    & python (Join-Path $scripts "phase_1_baseline.py") `
        --dataset $ds.name `
        --metadata $meta `
        --scores $scores `
        --unit-col $ds.unit `
        --condition-col "condition" `
        --ipf-value "IPF" `
        --ctrl-value "CTRL" `
        --top-n 20 `
        --n-perm 500 `
        --outdir (Join-Path $resDir "02_baseline/$($ds.name)")
}

# ═════════════════════════════════════════════════════════════
# [3/6] Phase 2: Matched Random Gene Set Control
# ═════════════════════════════════════════════════════════════
Write-Host "`n[3/6] Phase 2: Random Gene Set Control" -ForegroundColor Green
Assert-File (Join-Path $scripts "phase_2_matched_random.py")

foreach ($ds in $datasets) {
    $meta   = Join-Path $dataDir "$($ds.name)/metadata.csv"
    $scores = Join-Path $dataDir "$($ds.name)/pathway_scores.csv"
    $btp    = Join-Path $resDir "02_baseline/$($ds.name)/baseline_top_pathways.csv"

    if (-not ((Test-Path $scores) -and (Test-Path $btp))) {
        Write-Host "  SKIP Phase 2 ($($ds.name)): scores or baseline missing" -ForegroundColor Yellow
        continue
    }

    & python (Join-Path $scripts "phase_2_matched_random.py") `
        --dataset $ds.name `
        --metadata $meta `
        --scores $scores `
        --baseline-pathways $btp `
        --unit-col $ds.unit `
        --condition-col "condition" `
        --ipf-value "IPF" `
        --ctrl-value "CTRL" `
        --n-random 200 `
        --margin 0.05 `
        --seed 42 `
        --outdir (Join-Path $resDir "03_matched_random/$($ds.name)")
}

# ═════════════════════════════════════════════════════════════
# [4/6] Phase 3: Holdout Generalization
# ═════════════════════════════════════════════════════════════
Write-Host "`n[4/6] Phase 3: Holdout Generalization" -ForegroundColor Green
Assert-File (Join-Path $scripts "phase_3_holdout.py")

foreach ($ds in $datasets) {
    $meta   = Join-Path $dataDir "$($ds.name)/metadata.csv"
    $scores = Join-Path $dataDir "$($ds.name)/pathway_scores.csv"

    if (-not (Test-Path $scores)) {
        Write-Host "  SKIP Phase 3 ($($ds.name)): pathway_scores.csv missing" -ForegroundColor Yellow
        continue
    }

    & python (Join-Path $scripts "phase_3_holdout.py") `
        --dataset $ds.name `
        --metadata $meta `
        --scores $scores `
        --unit-col $ds.unit `
        --condition-col "condition" `
        --ipf-value "IPF" `
        --ctrl-value "CTRL" `
        --top-n 20 `
        --n-splits 50 `
        --n-perm 500 `
        --train-frac 0.7 `
        --outdir (Join-Path $resDir "04_holdout/$($ds.name)")
}

# ═════════════════════════════════════════════════════════════
# [5/6] Generate Publication Figures
# ═════════════════════════════════════════════════════════════
Write-Host "`n[5/6] Generating Figures" -ForegroundColor Green
Assert-File (Join-Path $scripts "make_figures.py")
& python (Join-Path $scripts "make_figures.py")

# ═════════════════════════════════════════════════════════════
# [6/6] Verify Manuscript Numbers
# ═════════════════════════════════════════════════════════════
Write-Host "`n[6/6] Verifying Manuscript Numbers" -ForegroundColor Green
Assert-File (Join-Path $scripts "verify_manuscript.py")
& python (Join-Path $scripts "verify_manuscript.py") | Tee-Object -FilePath (Join-Path $resDir "verification_report.txt")

# ── Done ────────────────────────────────────────────────────
$elapsed = (Get-Date) - (Get-Date).Date   # rough; fine for a report
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Pipeline Complete!" -ForegroundColor Cyan
Write-Host "Finished: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nResults available in:" -ForegroundColor Yellow
Write-Host "  results/01_audit/           - Phase 0 leakage audit" -ForegroundColor White
Write-Host "  results/02_baseline/        - Phase 1 baseline pathways" -ForegroundColor White
Write-Host "  results/03_matched_random/  - Phase 2 random controls" -ForegroundColor White
Write-Host "  results/04_holdout/         - Phase 3 holdout validation" -ForegroundColor White
Write-Host "  results/figures/            - Publication figures (PDF+PNG)" -ForegroundColor White
Write-Host "  results/verification_report.txt  - Number verification" -ForegroundColor White

