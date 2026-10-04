"""Clean the public multi-city restaurant CSV and retain Pune records only."""
from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "restaurants.csv"
OUT = ROOT / "data" / "processed"

def clean_text(value):
    if pd.isna(value):
        return pd.NA
    return re.sub(r"\s+", " ", str(value)).strip() or pd.NA

def to_number(series):
    return pd.to_numeric(series.astype("string").str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")

def clean_restaurants(source=RAW):
    df = pd.read_csv(source)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    required = {"name", "location", "city", "cuisine", "rating", "votes", "cost"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {sorted(missing)}")
    for col in ("name", "location", "city", "cuisine"):
        df[col] = df[col].map(clean_text)
    df["city"] = df["city"].str.casefold()
    df = df[df["city"].eq("pune")].copy()
    df["rating"] = to_number(df["rating"])
    df["votes"] = to_number(df["votes"])
    df["cost"] = to_number(df["cost"])
    # Unparseable/missing values remain null; impossible ratings are excluded as invalid.
    df.loc[~df["rating"].between(0, 5), "rating"] = pd.NA
    df.loc[df["votes"] < 0, "votes"] = pd.NA
    df.loc[df["cost"] <= 0, "cost"] = pd.NA
    df = df.dropna(subset=["name", "location"]).drop_duplicates(subset=["name", "location", "cuisine"], keep="first")
    # Stable within this exported snapshot; regenerates if source ordering changes.
    df = df.sort_values(["name", "location", "cuisine"], na_position="last").reset_index(drop=True)
    df.insert(0, "restaurant_key", range(1, len(df) + 1))
    df["price_category"] = pd.cut(df["cost"], [-float("inf"), 500, 1500, 3000, float("inf")], labels=["Budget", "Moderate", "Premium", "Luxury"])
    df["rating_category"] = pd.cut(df["rating"], [-float("inf"), 2.5, 3.5, 4.2, 5], labels=["Poor", "Average", "Good", "Excellent"], include_lowest=True)
    df["cuisine_count"] = df["cuisine"].fillna("").map(lambda x: sum(bool(s.strip()) for s in x.split(",")))
    df["popularity_category"] = pd.cut(df["votes"], [-float("inf"), 49, 199, 999, float("inf")], labels=["Few ratings", "Some ratings", "Popular", "Highly reviewed"])
    return df

def main():
    if not RAW.exists():
        raise FileNotFoundError(f"Place source CSV at {RAW}. See README for source and instructions.")
    OUT.mkdir(parents=True, exist_ok=True)
    df = clean_restaurants()
    df.to_csv(OUT / "pune_restaurants_cleaned.csv", index=False)
    # One row per restaurant-cuisine association supports accurate cuisine counts in BI.
    cuisines = df[["restaurant_key", "name", "location", "cuisine"]].dropna(subset=["cuisine"]).assign(cuisine=lambda x: x.cuisine.str.split(r"\s*,\s*")).explode("cuisine")
    cuisines["cuisine"] = cuisines["cuisine"].map(clean_text)
    cuisines.dropna(subset=["cuisine"]).to_csv(OUT / "restaurant_cuisines.csv", index=False)
    print(f"Input rows: {len(pd.read_csv(RAW)):,}; Pune cleaned rows: {len(df):,}; columns: {len(df.columns)}")
    print("Null counts:\n", df.isna().sum().to_string())
    print("Duplicate rows after cleaning:", int(df.duplicated().sum()))

if __name__ == "__main__":
    main()
