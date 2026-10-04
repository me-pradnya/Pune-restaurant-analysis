# Power BI Desktop implementation guide

## Status

This is a build specification. No `.pbix` was created or checked because Power BI Desktop is unavailable in the current environment.

## Import and model

1. Run the Python pipeline and import `data/processed/pune_restaurants_cleaned.csv` as `Restaurants` and `restaurant_cuisines.csv` as `RestaurantCuisines`.
2. The cleaning script exports a snapshot-stable integer `restaurant_key` in both tables.
3. Relate `Restaurants[restaurant_key]` (one) to `RestaurantCuisines[restaurant_key]` (many). To have cuisine slicers filter restaurant-level visuals, set cross-filter direction to Both and verify the interactions; alternatively keep single direction and make cuisine-specific visuals use the bridge only. Verify uniqueness on the one side after import.
4. Set rating and cost to decimal; votes/counts to whole number; text fields to text. Use `location`, `price_category`, `rating_category`, `cuisine` as categorical fields.
5. Add measures from `dax_measures.md`; use distinct restaurant count for all bridge-filtered charts.

## Suggested report pages

**Executive Overview:** KPI cards (restaurants, average rating, average cost for two, total votes, locations, cuisine types); bar chart of listings by locality; rating distribution; top cuisine tags; slicers for locality, cuisine, rating category and price category.

**Ratings & Popularity:** ranked restaurant table (rating, votes, cost; filter minimum 50 votes), scatter plot votes vs rating (votes log axis if practical), average rating by locality with rated-record count in tooltip, cuisine rating chart with minimum sample count filter.

**Pricing & Cuisine:** average cost by locality and cuisine, price category distribution, rating vs cost scatter; maintain clear sample counts in tooltips.

Slicers: location, cuisine, rating category and price category. Avoid online order/table booking/type slicers; these fields are not in the documented source. No map visual: coordinates are unavailable. Ensure slicers filter all intended visuals and check multi-cuisine counts do not inflate restaurant totals.

## Validation checklist

Compare unfiltered restaurant count, mean rating, mean cost and total votes with `data/processed/python_kpi_reference.json`. Confirm unique key, relationship direction, null handling, slicer interactions, and cuisine distinct count. Save as `powerbi/Pune_Restaurant_Analysis.pbix` and capture report screenshots only after Desktop validation.
