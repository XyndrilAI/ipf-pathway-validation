#!/usr/bin/env python3
"""
Generate robustness grid visualisations:
  1. Heatmap  (SI and p-value across TOP_N × seeds)
  2. Violin   (SI distribution per TOP_N with null baseline)

Usage:
  python plot_robustness.py <robustness_grid.csv>

Outputs are written next to the input CSV.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 10


def plot_robustness_heatmap(df: pd.DataFrame, output_path: Path) -> None:
    """Heatmap: SI and p-value across TOP_N × seed."""
    pivot_si = df.pivot(index="seed", columns="top_n", values="si_mean")
    pivot_p = df.pivot(index="seed", columns="top_n", values="empirical_p")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    sns.heatmap(
        pivot_si, annot=True, fmt=".3f", cmap="YlGnBu",
        ax=axes[0], cbar_kws={"label": "SI (Jaccard)"},
    )
    axes[0].set_title("Baseline SI across TOP_N × Seeds")
    axes[0].set_xlabel("TOP_N")
    axes[0].set_ylabel("Seed")

    sns.heatmap(
        pivot_p, annot=True, fmt=".3f", cmap="RdYlGn_r",
        vmin=0, vmax=0.1, ax=axes[1],
        cbar_kws={"label": "Empirical p-value"},
    )
    axes[1].set_title("Empirical p-value (vs permutation null)")
    axes[1].set_xlabel("TOP_N")
    axes[1].set_ylabel("Seed")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Heatmap saved: {output_path}")


def plot_sensitivity_bars(df: pd.DataFrame, output_path: Path) -> None:
    """Grouped bar chart: baseline SI vs null mean per TOP_N (averaged across seeds)."""
    summary = (
        df.groupby("top_n")
        .agg(
            si_mean=("si_mean", "mean"),
            si_std=("si_mean", "std"),
            null_mean=("null_mean", "mean"),
            null_std=("null_mean", "std"),
        )
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.arange(len(summary))
    width = 0.35

    bars1 = ax.bar(
        x - width / 2, summary["null_mean"], width,
        yerr=summary["null_std"], label="Null (permuted)", color="gray",
        alpha=0.7, capsize=5,
    )
    bars2 = ax.bar(
        x + width / 2, summary["si_mean"], width,
        yerr=summary["si_std"], label="Baseline (LOCO)", color="steelblue",
        alpha=0.7, capsize=5,
    )

    ax.set_xlabel("TOP_N")
    ax.set_ylabel("Separability Index (Jaccard)")
    ax.set_title("SI Sensitivity to TOP_N (mean ± SD across seeds)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"TOP_{n}" for n in summary["top_n"]])
    ax.legend()
    ax.set_ylim(0, 1)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Bar chart saved: {output_path}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python plot_robustness.py <robustness_grid.csv>")
        sys.exit(1)

    grid_csv = Path(sys.argv[1])
    if not grid_csv.exists():
        raise SystemExit(f"File not found: {grid_csv}")

    df = pd.read_csv(grid_csv)
    output_dir = grid_csv.parent

    plot_robustness_heatmap(df, output_dir / "robustness_heatmap.png")
    plot_robustness_heatmap(df, output_dir / "robustness_heatmap.pdf")
    plot_sensitivity_bars(df, output_dir / "robustness_sensitivity.png")
    plot_sensitivity_bars(df, output_dir / "robustness_sensitivity.pdf")


if __name__ == "__main__":
    main()

