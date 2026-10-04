"""Produce reproducible summaries, business findings and presentation-ready plots."""
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "pune_restaurants_cleaned.csv"
PLOTS = ROOT / "visualizations"
REPORT = ROOT / "documentation" / "analysis_results.md"

def main():
    df = pd.read_csv(DATA)
    PLOTS.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", palette="viridis")
    loc = df.groupby("location", dropna=True).agg(restaurants=("name", "size"), avg_rating=("rating", "mean"), avg_cost=("cost", "mean")).sort_values("restaurants", ascending=False)
    cuisine = pd.read_csv(ROOT / "data" / "processed" / "restaurant_cuisines.csv")
    cuisines = cuisine.groupby("cuisine").size().sort_values(ascending=False).head(15)
    top_locs = loc.head(15)
    fig, ax = plt.subplots(figsize=(11, 6)); top_locs["restaurants"].sort_values().plot.barh(ax=ax); ax.set(title="Pune restaurants by locality (top 15)", xlabel="Restaurant records", ylabel="Locality"); fig.tight_layout(); fig.savefig(PLOTS / "restaurants_by_location.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5)); sns.histplot(df["rating"].dropna(), bins=20, ax=ax); ax.set(title="Restaurant rating distribution", xlabel="Rating", ylabel="Records"); fig.tight_layout(); fig.savefig(PLOTS / "rating_distribution.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5)); sns.histplot(df["cost"].dropna(), bins=30, ax=ax); ax.set(title="Cost for two distribution", xlabel="Cost for two (source currency units)", ylabel="Records"); fig.tight_layout(); fig.savefig(PLOTS / "cost_distribution.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 6)); cuisines.sort_values().plot.barh(ax=ax); ax.set(title="Most frequent cuisine tags", xlabel="Restaurant-cuisine associations", ylabel="Cuisine"); fig.tight_layout(); fig.savefig(PLOTS / "top_cuisines.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5)); sns.scatterplot(data=df, x="cost", y="rating", size="votes", sizes=(10, 120), alpha=.5, ax=ax, legend=False); ax.set(title="Cost for two vs rating", xlabel="Cost for two", ylabel="Rating"); fig.tight_layout(); fig.savefig(PLOTS / "rating_vs_cost.png", dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5)); sns.scatterplot(data=df, x="votes", y="rating", alpha=.45, ax=ax); ax.set_xscale("symlog"); ax.set(title="Review volume vs rating", xlabel="Votes (symlog scale)", ylabel="Rating"); fig.tight_layout(); fig.savefig(PLOTS / "rating_vs_votes.png", dpi=180); plt.close(fig)
    # Require a meaningful sample before locality/cuisine comparisons; threshold is explicit.
    location_quality = df.groupby("location").agg(n=("rating", "count"), avg_rating=("rating", "mean"), avg_cost=("cost", "mean")).query("n >= 5").sort_values("avg_rating", ascending=False)
    eligible = df[df["votes"].fillna(0) >= 50].sort_values(["rating", "votes"], ascending=False).head(20)
    overview = {"restaurants": int(len(df)), "locations": int(df.location.nunique()), "cuisine_tags": int(cuisine.cuisine.nunique()), "average_rating": df.rating.mean(), "average_cost_for_two": df.cost.mean(), "total_votes": df.votes.sum(), "rating_cost_spearman": df[["rating", "cost"]].corr(method="spearman").iloc[0,1], "rating_votes_spearman": df[["rating", "votes"]].corr(method="spearman").iloc[0,1]}
    (ROOT / "data" / "processed" / "python_kpi_reference.json").write_text(json.dumps(overview, indent=2), encoding="utf-8")
    lines = ["# Calculated analysis results", "", "Generated from the current processed Pune data by `src/exploratory_analysis.py`.", "", "## Dataset KPIs", ""]
    lines += [f"- {k.replace('_',' ').title()}: {v:.3f}" if isinstance(v, float) and pd.notna(v) else f"- {k.replace('_',' ').title()}: {v}" for k,v in overview.items()]
    lines += ["", "## Largest localities", "", loc.head(10).round(2).to_markdown(), "", "## Highest average rating (localities with at least 5 rated records)", "", location_quality.head(10).round(2).to_markdown(), "", "## Top restaurants (minimum 50 votes)", "", eligible[["name","location","cuisine","rating","votes","cost"]].to_markdown(index=False), "", "## Interpretation", "", "Correlations are descriptive associations and do not imply causation. Locality rankings depend on this source's coverage and the minimum sample threshold."]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(overview, indent=2))

if __name__ == "__main__": main()
