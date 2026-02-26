#!/usr/bin/env python3
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
RESULTS = Path(r"D:\ipf_sprint\results")
original = pd.read_csv(RESULTS / "04_holdout" / "GSE53845" / "holdout_si.csv")
stratified = pd.read_csv(RESULTS / "stratified" / "GSE53845" / "stratified_holdout.csv")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ax = axes[0]
methods = ["Original", "Stratified"]
si_means = [original["holdout_si_mean"].values[0], stratified["holdout_si_mean"].values[0]]
null_means = [original["null_si_mean"].values[0], stratified["null_si_mean"].values[0]]
p_values = [original["empirical_p"].values[0], stratified["empirical_p"].values[0]]
x = np.arange(len(methods))
w = 0.35
ax.bar(x - w/2, null_means, w, label="Null", color="gray", alpha=0.7)
ax.bar(x + w/2, si_means, w, label="Observed", color="steelblue", alpha=0.7)
ax.set_ylabel("Separability Index"); ax.set_title("GSE53845: Original vs Stratified Null")
ax.set_xticks(x); ax.set_xticklabels(methods); ax.legend()
ax.set_ylim(0, max(si_means)+0.15); ax.grid(axis="y", alpha=0.3)
for i, p in enumerate(p_values):
    s = "PASS" if p < 0.05 else "borderline"
    ax.text(i, max(si_means[i], null_means[i])+0.03, f"p={p:.3f} ({s})", ha="center", fontsize=9)
ax = axes[1]
om = original["holdout_si_mean"].values[0]; os_ = original["holdout_si_std"].values[0]
sm = stratified["holdout_si_mean"].values[0]
cl = stratified["ci_lower_95"].values[0]; ch = stratified["ci_upper_95"].values[0]
ax.errorbar([0],[om],yerr=[os_],fmt="o",label="Original (SD)",ms=10,capsize=5,color="coral")
ax.errorbar([1],[sm],yerr=[[sm-cl],[ch-sm]],fmt="o",label="Stratified (95% CI)",ms=10,capsize=5,color="darkgreen")
ax.axhline(original["null_si_mean"].values[0],color="gray",ls="--",label="Orig Null",alpha=0.7)
ax.axhline(stratified["null_si_mean"].values[0],color="red",ls="--",label="Strat Null",alpha=0.7)
ax.set_ylabel("Separability Index"); ax.set_title("Effect Size with Uncertainty")
ax.set_xticks([0,1]); ax.set_xticklabels(["Original","Stratified"])
ax.legend(loc="best",fontsize=8); ax.grid(axis="y",alpha=0.3)
plt.tight_layout()
od = RESULTS / "stratified" / "GSE53845"
od.mkdir(parents=True, exist_ok=True)
plt.savefig(od / "borderline_fix_comparison.pdf", dpi=300, bbox_inches="tight")
plt.savefig(od / "borderline_fix_comparison.png", dpi=300, bbox_inches="tight")
print(f"Plot saved to {od}")
