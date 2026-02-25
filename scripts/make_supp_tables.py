#!/usr/bin/env python3
"""Generate Supplementary Tables S1 and S2 for PATH B paper."""
import pandas as pd
from pathlib import Path

paper = Path(r"D:\ipf_sprint\results\paper")

# ── Supplementary Table S1: Top-20 Pathways Across Both Cohorts ─────────

top_24206 = pd.read_csv(paper / "top20_pathways_GSE24206.csv")
top_53845 = pd.read_csv(paper / "top20_pathways_GSE53845.csv")

merged = top_24206.merge(
    top_53845,
    on="pathway",
    how="outer",
    suffixes=("_GSE24206", "_GSE53845"),
)

# Compute min rank for sorting before formatting
merged["_min_rank"] = merged[["rank_GSE24206", "rank_GSE53845"]].min(axis=1)
merged = merged.sort_values("_min_rank").reset_index(drop=True)

# Format for display
merged["rank_GSE24206"] = merged["rank_GSE24206"].apply(
    lambda x: str(int(x)) if pd.notna(x) else "--"
)
merged["rank_GSE53845"] = merged["rank_GSE53845"].apply(
    lambda x: str(int(x)) if pd.notna(x) else "--"
)
merged["effect_GSE24206"] = merged["effect_GSE24206"].apply(
    lambda x: f"{x:+.3f}" if pd.notna(x) else "--"
)
merged["effect_GSE53845"] = merged["effect_GSE53845"].apply(
    lambda x: f"{x:+.3f}" if pd.notna(x) else "--"
)

supp_s1 = merged[
    ["pathway", "rank_GSE24206", "effect_GSE24206", "rank_GSE53845", "effect_GSE53845"]
].copy()
supp_s1.columns = [
    "Pathway",
    "Rank (GSE24206)",
    "Effect (GSE24206)",
    "Rank (GSE53845)",
    "Effect (GSE53845)",
]

supp_s1.to_csv(paper / "supplementary_table_s1.csv", index=False)

with open(paper / "supplementary_table_s1.md", "w", encoding="utf-8") as f:
    f.write("# Supplementary Table S1: Top-20 Pathways Across Both Cohorts\n\n")
    f.write(supp_s1.to_markdown(index=False))
    f.write(
        "\n\nPathways ranked by absolute effect size (|mean_IPF - mean_Control|). "
        "Effect signs: positive = up in IPF, negative = down in IPF. "
        "'--' indicates pathway not in top-20 for that dataset.\n"
    )

print(f"Supplementary Table S1: {len(supp_s1)} unique pathways")
print(f"  -> {paper / 'supplementary_table_s1.csv'}")
print(f"  -> {paper / 'supplementary_table_s1.md'}")

# ── Supplementary Table S2: Cross-Cohort Overlap Analysis ───────────────

# Re-read originals (unformatted)
top_24206 = pd.read_csv(paper / "top20_pathways_GSE24206.csv")
top_53845 = pd.read_csv(paper / "top20_pathways_GSE53845.csv")

overlap_data = []
for cutoff in [5, 10, 15, 20]:
    set_24206 = set(top_24206.head(cutoff)["pathway"])
    set_53845 = set(top_53845.head(cutoff)["pathway"])
    intersection = set_24206 & set_53845
    union = set_24206 | set_53845
    jaccard = len(intersection) / len(union) if len(union) > 0 else 0

    if len(intersection) <= 5:
        common_str = ", ".join(sorted(intersection)) if intersection else "none"
    else:
        common_str = f"{len(intersection)} pathways (see Table S1)"

    overlap_data.append({
        "Rank Cutoff": f"Top-{cutoff}",
        "GSE24206 Pathways": len(set_24206),
        "GSE53845 Pathways": len(set_53845),
        "Overlap (n)": len(intersection),
        "Jaccard Index": f"{jaccard:.3f}",
        "Common Pathways": common_str,
    })

supp_s2 = pd.DataFrame(overlap_data)
supp_s2.to_csv(paper / "supplementary_table_s2.csv", index=False)

with open(paper / "supplementary_table_s2.md", "w", encoding="utf-8") as f:
    f.write("# Supplementary Table S2: Cross-Cohort Pathway Overlap\n\n")
    f.write(supp_s2.to_markdown(index=False))
    f.write(
        "\n\nJaccard Index = |A intersect B| / |A union B| "
        "where A and B are top-N pathway sets from each cohort.\n"
    )

print(f"\nSupplementary Table S2:")
print(f"  -> {paper / 'supplementary_table_s2.csv'}")
print(f"  -> {paper / 'supplementary_table_s2.md'}")
print("\nOverlap summary:")
for _, row in supp_s2.iterrows():
    print(f"  {row['Rank Cutoff']:8s}  overlap={row['Overlap (n)']}  Jaccard={row['Jaccard Index']}")

