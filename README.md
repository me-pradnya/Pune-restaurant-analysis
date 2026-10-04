# Pune Restaurant Analysis

An end-to-end Python and Power BI project template for analyzing Pune restaurant listings. The workflow is implemented as reproducible Python scripts; dataset-dependent metrics and findings are generated only after the source CSV is supplied.

## Business problem and objectives

Restaurant operators and customers need a clear view of how listings, cuisine mix, ratings, review volume and cost vary across Pune localities. This project prepares a reliable analysis of those patterns, including rating-versus-cost and rating-versus-vote associations. It is descriptive analysis and does not infer causation.

## Dataset

**Selected source:** [Kasurde / Indian Restaurants Data Analysis](https://github.com/Kasurde/Indian-Restaurants-Data-Analysis). Its README describes a CSV of 6,593 records across 23 Indian cities, including Pune, with Name, Location, Locality, City, Cuisine, Rating, Votes and Cost. The publisher describes the data as scraped; the exact collection date and coverage methodology are not stated. Treat it as a snapshot, not a complete or current census. The repository advertises GPL-3.0; verify source-file terms and attribution requirements before republishing the raw data.

The source CSV could not be downloaded in the current environment because the GitHub TLS connection failed. Therefore the raw/processed folders are intentionally unpopulated, no results are claimed, and the included data pipeline has not yet been run against real records. Download the source repository's `restaurants.csv` and place it at `data/raw/restaurants.csv`.

## Technologies

Python, Pandas, NumPy (dependency available for extensions), Matplotlib, Seaborn, Power BI Desktop and DAX. Git/GitHub can version the project. The implementation uses scripts rather than a notebook, which keeps the full run reproducible with one command.

## Workflow and analysis

Raw multi-city CSV → select Pune → clean text and numeric fields → deduplicate → derive price, rating, popularity and cuisine-count bands → export a restaurant table and restaurant-cuisine bridge → summaries, correlations, plots and business result report → import in Power BI.

Cleaning preserves missing values instead of imputing unsupported information. Ratings outside 0–5, negative votes and nonpositive costs are set to missing; they are not replaced by averages or zero. Duplicate key: name + location + cuisine. Potential cost/vote outliers are retained. Price bands (≤500, 501–1,500, 1,501–3,000, >3,000) and vote bands (<50, 50–199, 200–999, ≥1,000) are transparent analytical groupings, not source labels. Cuisine count counts comma-separated tags.

EDA calculates restaurant counts by locality, cuisine frequency, rating/cost distributions, top rated restaurants with at least 50 votes, locality ratings with at least five rated records, and Spearman associations between rating/cost and rating/votes. Script outputs are generated from supplied data, not hard-coded claims.

## Power BI implementation status

No `.pbix` was created or validated in this environment (Power BI Desktop was not detected). The exact manual model and layout are in [`powerbi/powerbi_implementation_guide.md`](powerbi/powerbi_implementation_guide.md); DAX drafts are in [`powerbi/dax_measures.md`](powerbi/dax_measures.md). Import `pune_restaurants_cleaned.csv` and `restaurant_cuisines.csv`; relate on a stable restaurant key after verifying uniqueness (the source has no persistent ID). Follow the bridge-table note in the guide to avoid inflated counts.

## Project structure

```text
outputs/
├── data/raw/                 # Add source restaurants.csv here
├── data/processed/           # Created by pipeline
├── src/                      # Cleaning, EDA and orchestration scripts
├── visualizations/           # PNG charts created by EDA
├── powerbi/                  # DAX and Desktop build guide
├── documentation/            # Methodology and generated results
├── requirements.txt
└── README.md
```

## Setup and run

From this `outputs` folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# Download restaurants.csv from the linked source repository into data/raw/
python src/data_preparation.py
```

The pipeline writes `data/processed/pune_restaurants_cleaned.csv`, `restaurant_cuisines.csv`, `python_kpi_reference.json`, `documentation/analysis_results.md`, and PNGs under `visualizations/`. Open Power BI Desktop, follow the implementation guide, create the visuals/measures, and save the report as `powerbi/Pune_Restaurant_Analysis.pbix`.

## Limitations and future improvements

Source collection date and representativeness are unclear; rating and cost semantics depend on the publisher's capture; locality names may be inconsistent. The source does not list online-order, booking, restaurant category, latitude, longitude or temporal fields, so these are excluded. Cuisine parsing assumes comma separators. A future revision can add a stable source ID, validation against current listings, improved locality normalization, geo coordinates from a licensed source, and an actual Desktop-built dashboard.

## Portfolio status

The scripts, project methodology, Power BI specification and DAX drafts are created. The data-derived analysis, chart outputs and PBIX remain pending the source CSV and Power BI Desktop, so this repository is not yet a completed evidence-backed portfolio project.
