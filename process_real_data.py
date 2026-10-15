import pandas as pd
import numpy as np

# Load the real Amazon data
df = pd.read_csv("amazon.csv")

print("Original columns:", df.columns.tolist())
print("Total rows:", len(df))

# Clean price and rating columns
df["discounted_price"] = df["discounted_price"].astype(str).str.replace("₹", "").str.replace(",", "").astype(float)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")

# Drop rows with missing important values
df = df.dropna(subset=["rating", "rating_count", "discounted_price", "review_content"])

# Create product-level data (one row per product)
products = df.groupby("product_id").agg({
    "product_name": "first",
    "category": "first",
    "discounted_price": "first",
    "rating": "mean",
    "rating_count": "sum"
}).reset_index()

# Clean category names (take only the first part)
products["category"] = products["category"].astype(str).str.split("|").str[0]

# Create simple demand and competition proxies
category_counts = products["category"].value_counts().to_dict()
products["demand_score"] = (products["rating_count"] / products["rating_count"].max() * 9 + 1).round(1)
products["competition_score"] = products["category"].map(lambda x: min(10, category_counts.get(x, 1) / 20)).round(1)

products = products.rename(columns={
    "product_id": "product_id",
    "product_name": "product_name",
    "category": "category",
    "discounted_price": "price",
    "rating": "avg_rating",
    "rating_count": "review_count"
})

products["product_id"] = range(1, len(products) + 1)
products = products[["product_id", "product_name", "category", "price", "avg_rating", "review_count", "competition_score", "demand_score"]]

# Create reviews data
reviews = df[["product_id", "review_content", "rating"]].copy()
reviews = reviews.rename(columns={"review_content": "review_text"})
reviews["review_id"] = range(1, len(reviews) + 1)
reviews["review_date"] = "2023-01-01"
reviews["product_id"] = reviews["product_id"].map(
    dict(zip(df.groupby("product_id").groups.keys(), range(1, len(products) + 1)))
)

# Save files
products.to_csv("real_products.csv", index=False)
reviews.to_csv("real_reviews.csv", index=False)

print(f"Created real_products.csv with {len(products)} products")
print(f"Created real_reviews.csv with {len(reviews)} reviews")
print("\nSample products:")
print(products.head())
