# Project documentation

## Objective and business problem

Describe Pune restaurant patterns across localities, ratings, cost, cuisines and review volume so customers and operators can compare the recorded market. Findings are descriptive and limited to the source snapshot.

## Dataset and data dictionary

Source: [Kasurde / Indian Restaurants Data Analysis](https://github.com/Kasurde/Indian-Restaurants-Data-Analysis), `restaurants.csv`; publisher documents 6,593 records across 23 cities, including Pune. Exact time period and collection procedure are not specified. Planned source columns:

| Field | Meaning | Treatment |
|---|---|---|
| Name | Restaurant listing name | Trim whitespace; required for retained row |
| Location | Locality/address field as supplied | Trim whitespace; required for retained row |
| Locality | Additional locality, if present | Retained when source has it |
| City | City | Case-normalized; filter Pune |
| Cuisine | Comma-separated cuisine tags | Trim; count tags and create bridge table |
| Rating | Reported rating | Numeric; outside 0–5 invalidated |
| Votes | Number of votes | Numeric; negative values invalidated |
| Cost | Approximate cost for two | Numeric parse; nonpositive value invalidated |

Some values may be missing. Additional source columns, if present, are preserved. The dataset has not been downloaded in this execution, so actual row/column counts after filtering cannot yet be stated.

## Cleaning and feature engineering

`src/data_cleaning.py` normalizes header names, strips/collapses text whitespace, filters city to Pune, parses rating/votes/cost numerically and preserves unparseable data as null. Rows without name or location are removed. Exact duplicate key is name + location + cuisine. Outliers remain for analysis; only impossible values listed above are invalidated.

Derived features: cost-based price category (Budget ≤500; Moderate 501–1,500; Premium 1,501–3,000; Luxury >3,000), rating category (Poor ≤2.5; Average >2.5–3.5; Good >3.5–4.2; Excellent >4.2–5), comma-separated cuisine count, and vote-based popularity band (<50, 50–199, 200–999, ≥1,000). These cutoffs are transparent project conventions, not claims about market standards.

## EDA and analytical questions

`src/exploratory_analysis.py` produces locality counts and averages, cuisine frequency, rating and cost distributions, top listings after a 50-vote minimum, locality rating comparisons after a minimum of five rated listings, and Spearman rank correlations for rating with cost and votes. It writes results into `documentation/analysis_results.md` and a machine-readable KPI reference. The minimum-vote and locality thresholds reduce tiny-sample noise but do not eliminate source bias.

Plots written: restaurants by locality, rating distribution, cost distribution, top cuisine tags, rating vs cost, rating vs votes. Relationship results describe association only. Business questions are answered by these generated tables and KPIs; there are no findings until actual source data is processed.

## Power BI data preparation and model

Exports: `data/processed/pune_restaurants_cleaned.csv` (one listing record per deduplicated key) and `restaurant_cuisines.csv` (one row per listing-cuisine association). Since source has no stable restaurant ID, validate or add a generated key in Power Query before joining bridge rows. Keep restaurant-level measures on the restaurant table. Use distinct listing key when analyzing cuisine bridge to prevent multi-cuisine restaurants from being double-counted. Full model/layout instructions: `powerbi/powerbi_implementation_guide.md`.

## DAX measures

Draft measures are in `powerbi/dax_measures.md`. Confirm column types, key uniqueness and filter behavior in Power BI Desktop. Cross-check unfiltered cards with `python_kpi_reference.json`.

## Assumptions and limitations

The CSV's `Cost` is interpreted as approximate cost for two, as documented by source. City text is interpreted literally as Pune after case folding. Cuisine values are split on commas. Cutoff boundaries are project choices. Missing values are not imputed. Outliers are retained. The dataset's age, scrape coverage, source sampling, rating platform, deduplication logic and precise currency semantics are not independently verified. No location coordinates, ordering/booking fields, category, or time series are documented; no map, temporal trend, or those measures are claimed.

## Reproduction

Install `requirements.txt`, download the documented source CSV into `data/raw/restaurants.csv`, and run `python src/data_preparation.py`. Inspect generated outputs and then implement the dashboard using the included guide. Power BI Desktop is a separate manual step; this environment did not create a PBIX.

## Future improvements

Obtain source metadata and explicit data license confirmation, build a stable ID, normalize locality aliases using a documented lookup, test edge cases with a small controlled dataset, acquire properly licensed coordinates, compare against a dated second snapshot, and create/validate the PBIX in Desktop.
