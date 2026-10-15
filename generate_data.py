import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

categories = ["Electronics", "Home & Kitchen", "Fashion", "Beauty", "Books", "Sports"]
products = []
reviews = []

product_id = 1
for cat in categories:
    for i in range(8):
        name = f"{cat} Product {i+1}"
        price = round(np.random.uniform(200, 5000), 2)
        rating = round(np.random.uniform(2.5, 4.8), 1)
        review_count = int(np.random.randint(20, 800))
        competition_score = round(np.random.uniform(1, 10), 1)
        demand_score = round(np.random.uniform(3, 10), 1)

        products.append({
            "product_id": product_id,
            "product_name": name,
            "category": cat,
            "price": price,
            "avg_rating": rating,
            "review_count": review_count,
            "competition_score": competition_score,
            "demand_score": demand_score
        })

        for r in range(min(15, review_count)):
            stars = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.1, 0.15, 0.3, 0.35])
            if stars >= 4:
                text = random.choice([
                    "Great product, highly recommend!",
                    "Excellent quality and fast delivery.",
                    "Perfect for daily use, very happy.",
                    "Worth the price, works as expected.",
                    "Amazing value, will buy again."
                ])
            elif stars == 3:
                text = random.choice([
                    "Average product, okay for the price.",
                    "Does the job but nothing special.",
                    "Mixed experience, some issues.",
                    "Decent but could be better."
                ])
            else:
                text = random.choice([
                    "Poor quality, disappointed.",
                    "Broke after a few days.",
                    "Not worth the money.",
                    "Bad experience, would not recommend.",
                    "Delivery was slow and product damaged."
                ])
            reviews.append({
                "review_id": len(reviews) + 1,
                "product_id": product_id,
                "rating": stars,
                "review_text": text,
                "review_date": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")
            })
        product_id += 1

products_df = pd.DataFrame(products)
reviews_df = pd.DataFrame(reviews)

products_df.to_csv("products.csv", index=False)
reviews_df.to_csv("reviews.csv", index=False)

print(f"Generated {len(products_df)} products and {len(reviews_df)} reviews")
print("Files created: products.csv and reviews.csv")
