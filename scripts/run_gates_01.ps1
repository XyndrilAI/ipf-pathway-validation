# run_gates_01.ps1
# Gate-ajojen pääskripti (Phase 0 aina, Phase 1 jos pathway_scores.csv löytyy)
$ErrorActionPreference = "Stop"

Write-Host "run_gates_01.ps1 käynnistyy..." -ForegroundColor Cyan
Write-Host "PSScriptRoot: $PSScriptRoot"
Write-Host "Working directory: $(Get-Location)"
Write-Host "PowerShell version: $($PSVersionTable.PSVersion)"

# Resolve paths robustly (no dependency on working directory)
$root    = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$scripts = (Resolve-Path $PSScriptRoot).Path
$dataDir = Join-Path $root "data"
$resDir  = Join-Path $root "results"

# Ensure results folders exist
New-Item -ItemType Directory -Force -Path (Join-Path $resDir "01_audit")        | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $resDir "02_baseline")     | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $resDir "03_matched_random") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $resDir "04_holdout")         | Out-Null

# Dataset definitions (GSE135893 dropped – no scRNA data available yet)
$datasets = @(
  @{ name="GSE24206";  mode="bulk"; unit="subject_id" },
  @{ name="GSE53845";  mode="bulk"; unit="subject_id" }
  # @{ name="GSE135893"; mode="scrna"; unit="donor_id"; library="library_id" }  # parked – scRNA pivot pending
)

foreach ($ds in $datasets) {
  Write-Host "`n=== Processing $($ds.name) [$($ds.mode)] ===" -ForegroundColor Green

  $meta   = Join-Path $dataDir "$($ds.name)\metadata.csv"
  $scores = Join-Path $dataDir "$($ds.name)\pathway_scores.csv"

  if (-not (Test-Path $meta)) {
    throw "Missing metadata: $meta"
  }

  # Output dirs per dataset
  $auditOut   = Join-Path $resDir "01_audit\$($ds.name)"
  $baseOut    = Join-Path $resDir "02_baseline\$($ds.name)"
  New-Item -ItemType Directory -Force -Path $auditOut | Out-Null
  New-Item -ItemType Directory -Force -Path $baseOut  | Out-Null

  # Phase 0
  if ($ds.mode -eq "bulk") {
    & python (Join-Path $scripts "phase_0_audit.py") `
      --dataset $ds.name `
      --metadata $meta `
      --mode bulk `
      --subject-col $ds.unit `
      --outdir $auditOut
  } else {
    & python (Join-Path $scripts "phase_0_audit.py") `
      --dataset $ds.name `
      --metadata $meta `
      --mode scrna `
      --donor-col $ds.unit `
      --library-col $ds.library `
      --outdir $auditOut
  }

  # Phase 1 (only if scores exist)
  if (Test-Path $scores) {
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
      --outdir $baseOut
  } else {
    Write-Host "SKIP Phase 1: scores missing -> $scores" -ForegroundColor Yellow
  }

  # Phase 2 (only if baseline_top_pathways.csv + scores exist)
  $baselinePathways = Join-Path $baseOut "baseline_top_pathways.csv"
  $matchedOut       = Join-Path $resDir "03_matched_random\$($ds.name)"
  New-Item -ItemType Directory -Force -Path $matchedOut | Out-Null

  if ((Test-Path $scores) -and (Test-Path $baselinePathways)) {
    & python (Join-Path $scripts "phase_2_matched_random.py") `
      --dataset $ds.name `
      --metadata $meta `
      --scores $scores `
      --baseline-pathways $baselinePathways `
      --unit-col $ds.unit `
      --condition-col "condition" `
      --ipf-value "IPF" `
      --ctrl-value "CTRL" `
      --n-random 200 `
      --margin 0.05 `
      --seed 42 `
      --outdir $matchedOut
  } else {
    Write-Host "SKIP Phase 2: baseline pathways or scores missing" -ForegroundColor Yellow
  }

  # Phase 3 (only if scores exist)
  $holdoutOut = Join-Path $resDir "04_holdout\$($ds.name)"
  New-Item -ItemType Directory -Force -Path $holdoutOut | Out-Null

  if (Test-Path $scores) {
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
      --outdir $holdoutOut
  } else {
    Write-Host "SKIP Phase 3: scores missing -> $scores" -ForegroundColor Yellow
  }
}

Write-Host "`nrun_gates_01.ps1 valmis. Tulokset: $resDir" -ForegroundColor Cyan
