#!/usr/bin/env python3
"""Generate publication figures for PATH B validation.

Figure 1: Phase 2 - Baseline SI vs Random null distribution
Figure 2: Phase 3 - Holdout SI vs Permutation null
"""
import matplotlib
matplotlib.use("Agg")  # headless backend for CI/server

import pandas as pd
import matplotlib.pyplot as plt

try:
    import seaborn as sns
    sns.set_style("whitegrid")
except ImportError:
    pass  # fallback to default style

from pathlib import Path

# Configure
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 10

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = SCRIPT_DIR.parent / "results"
FIG_DIR = RESULTS_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)

DATASETS = ["GSE24206", "GSE53845"]

# ============= FIGURE 1: Phase 2 - Baseline SI vs Random Null =============
print("Generating Figure 1: Phase 2 Baseline vs Random...")

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

for i, ds in enumerate(DATASETS):
    matched = pd.read_csv(RESULTS_DIR / "03_matched_random" / ds / "matched_random_si.csv")
    rand_dist = pd.read_csv(RESULTS_DIR / "03_matched_random" / ds / "random_si_distribution.csv")

    ax = axes[i]

    baseline_si = matched["baseline_SI"].values[0]
    random_mean = matched["random_mean_SI"].values[0]
    random_std = matched["random_std_SI"].values[0]
    delta = matched["delta"].values[0]
    emp_p = matched["empirical_p"].values[0]

    # Histogram of random SI values
    ax.hist(rand_dist["random_SI"].values, bins=25, color="lightgray",
            edgecolor="gray", alpha=0.8, label="Random sets (n=200)", density=False)

    # Vertical line for baseline
    ax.axvline(baseline_si, color="steelblue", linewidth=2.5, linestyle="-",
               label=f"Baseline SI = {baseline_si:.3f}")

    # Vertical line for random mean
    ax.axvline(random_mean, color="gray", linewidth=1.5, linestyle="--",
               label=f"Random mean = {random_mean:.3f}")

    ax.set_xlabel("Separability Index (SI)")
    ax.set_ylabel("Count")
    ax.set_title(f"{ds}\nBaseline vs Random Pathway Sets")
    ax.legend(fontsize=8, loc="upper right")

    # Delta annotation
    ax.text(0.03, 0.95,
            f"Delta = {delta:.3f}\np = {emp_p:.3f}",
            ha="left", va="top", transform=ax.transAxes, fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))

plt.suptitle("Figure 1: Phase 2 - Baseline Top-20 Pathways vs Random Sets",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(FIG_DIR / "figure1_phase2_baseline_vs_random.png", dpi=300, bbox_inches="tight")
plt.savefig(FIG_DIR / "figure1_phase2_baseline_vs_random.pdf", bbox_inches="tight")
plt.close()
print("  -> Saved figure1_phase2_baseline_vs_random.png|pdf")

# ============= FIGURE 2: Phase 3 - Holdout SI vs Null =============
print("Generating Figure 2: Phase 3 Holdout vs Null...")

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

for i, ds in enumerate(DATASETS):
    holdout = pd.read_csv(RESULTS_DIR / "04_holdout" / ds / "holdout_si.csv")

    ax = axes[i]

    ho_mean = holdout["holdout_si_mean"].values[0]
    ho_std = holdout["holdout_si_std"].values[0]
    null_mean = holdout["null_si_mean"].values[0]
    null_std = holdout["null_si_std"].values[0]
    si_diff = holdout["si_diff"].values[0]
    emp_p = holdout["empirical_p"].values[0]

    # Bar plot: null vs holdout
    bars = ax.bar(
        [0, 1],
        [null_mean, ho_mean],
        yerr=[null_std, ho_std],
        color=["#AAAAAA", "#4C8C4A" if emp_p < 0.05 else "#DAA520"],
        edgecolor=["#666666", "#2E5E2C" if emp_p < 0.05 else "#B8860B"],
        alpha=0.85,
        capsize=6,
        width=0.5,
    )

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Null\n(permuted labels)", "Holdout\n(70/30 split)"])
    ax.set_ylabel("Separability Index (Jaccard)")
    ax.set_title(f"{ds}\nHoldout Generalization")
    ax.set_ylim(0, 0.8)

    # Status annotation
    status = "PASS" if emp_p < 0.05 else "BORDERLINE"
    color = "lightgreen" if emp_p < 0.05 else "lightyellow"
    ax.text(0.5, 0.95,
            f"Delta = {si_diff:.3f}\np = {emp_p:.3f}\n{status}",
            ha="center", va="top", transform=ax.transAxes, fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.8))

plt.suptitle("Figure 2: Phase 3 - Holdout SI vs Permutation Null",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(FIG_DIR / "figure2_phase3_holdout.png", dpi=300, bbox_inches="tight")
plt.savefig(FIG_DIR / "figure2_phase3_holdout.pdf", bbox_inches="tight")
plt.close()
print("  -> Saved figure2_phase3_holdout.png|pdf")

print(f"\nAll figures saved to: {FIG_DIR}")

