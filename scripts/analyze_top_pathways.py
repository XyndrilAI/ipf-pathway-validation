#!/usr/bin/env python3
"""Analyze top-20 pathways per dataset and compute cross-cohort overlap."""
import pandas as pd
import numpy as np
from pathlib import Path

def compute_effect(path_scores, labels):
    ipf = path_scores[labels == 1].mean(axis=0)
    ctrl = path_scores[labels == 0].mean(axis=0)
    return ipf - ctrl

def analyze_top_pathways(dataset_name, metadata_path, scores_path):
    md = pd.read_csv(metadata_path)
    sc = pd.read_csv(scores_path)
    df = md.merge(sc, on="sample_id", how="inner")

    cond = df["condition"].astype(str)
    y = np.where(cond == "IPF", 1, np.where(cond == "CTRL", 0, np.nan)).astype(int)

    score_cols = [c for c in sc.columns if c != "sample_id"]
    scores = df[score_cols].apply(pd.to_numeric, errors="coerce").dropna(axis=1, how="all")

    global_effect = compute_effect(scores, pd.Series(y, index=df.index))
    top20 = global_effect.abs().sort_values(ascending=False).head(20)

    results = pd.DataFrame({
        "pathway": top20.index,
        "effect": global_effect[top20.index].values,
        "abs_effect": top20.values,
        "rank": range(1, 21),
    })
    return results

root = Path(r"D:\ipf_sprint")

top_24206 = analyze_top_pathways(
    "GSE24206",
    root / "data/GSE24206/metadata.csv",
    root / "data/GSE24206/pathway_scores.csv",
)
top_53845 = analyze_top_pathways(
    "GSE53845",
    root / "data/GSE53845/metadata.csv",
    root / "data/GSE53845/pathway_scores.csv",
)

paper = root / "results/paper"
top_24206.to_csv(paper / "top20_pathways_GSE24206.csv", index=False)
top_53845.to_csv(paper / "top20_pathways_GSE53845.csv", index=False)

print("=== GSE24206 Top-10 ===")
for _, r in top_24206.head(10).iterrows():
    direction = "UP in IPF" if r["effect"] > 0 else "DOWN in IPF"
    print(f"  {int(r['rank']):2d}. {r['pathway']:50s}  effect={r['effect']:+.4f}  ({direction})")

print("\n=== GSE53845 Top-10 ===")
for _, r in top_53845.head(10).iterrows():
    direction = "UP in IPF" if r["effect"] > 0 else "DOWN in IPF"
    print(f"  {int(r['rank']):2d}. {r['pathway']:50s}  effect={r['effect']:+.4f}  ({direction})")

# Overlap
o10 = set(top_24206["pathway"].head(10)) & set(top_53845["pathway"].head(10))
o20 = set(top_24206["pathway"].head(20)) & set(top_53845["pathway"].head(20))
print(f"\nTop-10 overlap: {len(o10)}/10 pathways: {sorted(o10)}")
print(f"Top-20 overlap: {len(o20)}/20 pathways: {sorted(o20)}")

