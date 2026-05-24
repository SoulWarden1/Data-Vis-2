import pandas as pd

# Load the data
cafes = pd.read_csv("data/cafes_by_locality.csv")
population = pd.read_csv("data/population_by_suburb.csv")

# Merge the data
pop_vs_cafes = cafes.merge(population, left_on="LOCALITY", right_on="Suburb", how="inner")

# Calculate café density (cafés per 1000 people)
pop_vs_cafes["cafe_density"] = (pop_vs_cafes["cafe_count"] / pop_vs_cafes["Population"]) * 1000

# Keep relevant columns
pop_vs_cafes = pop_vs_cafes[["LOCALITY", "cafe_count", "Population", "cafe_density"]].copy()
pop_vs_cafes = pop_vs_cafes.sort_values("Population", ascending=False)

# Save to CSV
pop_vs_cafes.to_csv("data/population_vs_cafes.csv", index=False)

# Display the data
pop_vs_cafes
