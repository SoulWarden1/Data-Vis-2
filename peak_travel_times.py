import pandas as pd

# Load the VISTA data
trips = pd.read_csv("data/trips_vista_2024_2025.csv")

# Filter for cafe trips: destination is restaurant/cafe and purpose is eating/drinking
cafe_trips = trips[
    (trips["destplace2"] == "Restaurant or Cafe") &
    (trips["destpurp2"] == "Ate or drank")
].copy()

# Convert triptime and cumdist to numeric, handling non-numeric values
cafe_trips["triptime"] = pd.to_numeric(cafe_trips["triptime"], errors="coerce")
cafe_trips["cumdist"] = pd.to_numeric(cafe_trips["cumdist"], errors="coerce")

# Group by start hour to get peak times
peak_times = cafe_trips.groupby("starthour").agg({
    "tripid": "count",  # number of trips
    "triptime": ["mean", "median"],  # average and median travel time
    "cumdist": "mean"  # average distance
}).reset_index()

# Flatten the column names
peak_times.columns = ["Hour", "TripCount", "AvgTravelTime", "MedianTravelTime", "AvgDistance"]

# Sort by hour
peak_times = peak_times.sort_values("Hour")

# Save to CSV
peak_times.to_csv("data/peak_cafe_travel_times.csv", index=False)

print(peak_times)
