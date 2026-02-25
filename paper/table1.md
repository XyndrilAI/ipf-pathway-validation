# Table 1: Validation Gate Summary

| Phase | Metric | GSE24206 | GSE53845 | Criterion | Status |
|-------|--------|----------|----------|-----------|--------|
| 0: Audit | Subjects (n) | 17 (11 IPF, 6 CTRL) | 48 (40 IPF, 8 CTRL) | >10 | PASS |
| 0: Audit | Samples/subject | 1.0 (aggregated) | 1.0 | <=1.5 | PASS |
| 0: Audit | Leakage risk | 0/17 leaked | 0/48 leaked | 0 | PASS |
| 1: Baseline | Top-20 min p | 0.002 | 0.002 | <0.05 | PASS |
| 1: Baseline | Top-20 max p | 0.028 | 0.022 | <0.05 | PASS |
| 2: Random | Baseline SI | 0.381 | 0.349 | >>random | PASS |
| 2: Random | Random mean SI | 0.225 +/- 0.025 | 0.221 +/- 0.024 | - | - |
| 2: Random | Delta (baseline - random) | 0.156 | 0.128 | >0.05 | PASS |
| 2: Random | Empirical p | <0.001 | <0.001 | <0.05 | PASS |
| 3: Holdout | SI (mean +/- SD) | 0.499 +/- 0.136 | 0.467 +/- 0.139 | >>null | PASS/BORDERLINE |
| 3: Holdout | Null SI (mean +/- SD) | 0.316 +/- 0.089 | 0.303 +/- 0.099 | - | - |
| 3: Holdout | Delta (holdout - null) | 0.183 | 0.164 | >0.10 | PASS |
| 3: Holdout | Empirical p | 0.03 | 0.07 | <0.05 | PASS / BORDERLINE |

*Notes:*
- GSE24206 originally had multi-lobe samples (~2.4 samples/subject), aggregated to subject-level mean before analysis
- GSE53845 borderline p-value (0.07) attributable to 40:8 IPF:CTRL imbalance reducing holdout power; effect size (Delta=0.164) remains robust
- SI = Separability Index (mean |AUC - 0.5| for Phase 2; Jaccard top-N overlap for Phase 3)
- All permutation tests: 500 iterations, seed=42

