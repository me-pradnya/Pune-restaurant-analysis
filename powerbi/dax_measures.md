# DAX measures

Assumptions: restaurant-level table is named `Restaurants`; its rows have been deduplicated, and a unique `RestaurantKey` has been generated in Power Query. Column names correspond to the cleaned CSV. Review data types and exact names after import.

```DAX
Total Restaurants = DISTINCTCOUNT(Restaurants[RestaurantKey])

Average Rating = AVERAGE(Restaurants[rating])

Average Cost for Two = AVERAGE(Restaurants[cost])

Total Votes = SUM(Restaurants[votes])

Average Votes per Restaurant = AVERAGE(Restaurants[votes])

Highly Rated Restaurants =
CALCULATE([Total Restaurants], Restaurants[rating] >= 4)

Highly Rated Share =
DIVIDE([Highly Rated Restaurants], [Total Restaurants])

Locations = DISTINCTCOUNT(Restaurants[location])

Cuisine Types = DISTINCTCOUNT(RestaurantCuisines[cuisine])

Rank by Rating =
RANKX(ALLSELECTED(Restaurants[name]), [Average Rating], , DESC, DENSE)
```

Votes are a sum of source vote counts per listing; they should not be described as unique customers. Cuisine type count uses the bridge table. Avoid counting bridge rows as restaurants; use distinct restaurant key. Verify the threshold of 4 as a report convention. The Python reference KPIs use non-null mean rating/cost and sum of non-null votes; compare with equivalent unfiltered DAX cards.
