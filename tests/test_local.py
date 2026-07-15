"""
Standalone test for Member 4's agents (Comparison + Recommendation).

Why this exists: the Search Agent / Amazon / Flipkart / Firecrawl services
don't exist in the repo yet, so there's no real way to get a `products` list
to test with. This script fakes that input with realistic mock data so you
can verify your two agents work correctly, right now, independently.

Run:
    python tests/test_local.py

(Run this from the repo root so the `Agents.` and `utils.` imports resolve.)
"""

import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Agents.comparison_agent import comparison_agent
from Agents.recommendation_agent import recommendation_agent


MOCK_PRODUCTS = [
    {"name": "iPhone 15 128GB Blue", "price": 65999, "rating": 4.6, "reviews": 12500,
     "seller": "Appario Retail", "url": "https://amazon.in/x1", "image_url": "", "source": "Amazon",
     "delivery_info": "Free delivery by tomorrow", "specifications": "128GB, 6.1-inch, A16 Bionic", "brand": "Apple"},
    {"name": "Apple iPhone 15 (128 GB) - Blue", "price": 64999, "rating": 4.5, "reviews": 8300,
     "seller": "RetailNet", "url": "https://flipkart.com/x2", "image_url": "", "source": "Flipkart",
     "delivery_info": "Delivery in 2 days", "specifications": "128GB, 6.1-inch, A16 Bionic", "brand": "Apple"},
    {"name": "Samsung Galaxy S24 128GB", "price": 59999, "rating": 4.4, "reviews": 6100,
     "seller": "Samsung India", "url": "https://amazon.in/x3", "image_url": "", "source": "Amazon",
     "delivery_info": "Free delivery", "specifications": "128GB, 6.2-inch, Snapdragon 8 Gen 3", "brand": "Samsung"},
    {"name": "Samsung Galaxy S24 5G 128GB", "price": 57499, "rating": 4.3, "reviews": 4200,
     "seller": "SuperComNet", "url": "https://flipkart.com/x4", "image_url": "", "source": "Flipkart",
     "delivery_info": "Delivery in 3 days", "specifications": "128GB, 6.2-inch, Snapdragon 8 Gen 3", "brand": "Samsung"},
    {"name": "OnePlus 12 256GB", "price": 64999, "rating": 4.5, "reviews": 3100,
     "seller": "OnePlus Store", "url": "https://amazon.in/x5", "image_url": "", "source": "Amazon",
     "delivery_info": "Free delivery", "specifications": "256GB, 6.82-inch, Snapdragon 8 Gen 3", "brand": "OnePlus"},
    {"name": "Suspiciously Cheap iPhone 15 Clone", "price": 4999, "rating": 3.1, "reviews": 40,
     "seller": "Unknown Seller", "url": "https://other-store.com/x6", "image_url": "", "source": "Other",
     "delivery_info": "7-10 days", "specifications": "Unverified", "brand": "Apple"},
]


def run_case(label: str, state: dict):
    print(f"\n{'=' * 70}\n{label}\n{'=' * 70}")

    comp_out = comparison_agent(state)
    state.update(comp_out)

    rec_out = recommendation_agent(state)
    state.update(rec_out)

    print(f"\n-- Comparison summary --")
    cd = state["comparison_data"]
    if cd:
        print(f"Total products after filters: {cd['total_products']}")
        print(f"Cheapest: {cd['cheapest']['name']} @ ₹{cd['cheapest']['price']:,}" if cd.get('cheapest') else "Cheapest: none")
        print(f"Highest rated: {cd['highest_rated']['name']} ({cd['highest_rated']['rating']}⭐)" if cd.get('highest_rated') else "Highest rated: none")
        print(f"Best value: {cd['best_value']['name']} (score {cd['best_value']['value_score']:.1f})" if cd.get('best_value') else "Best value: none")
        if cd.get("outliers"):
            print(f"⚠ Outliers flagged: {[o['name'] for o in cd['outliers']]}")
    else:
        print("No comparison data (no products matched).")

    print(f"\n-- Top recommendations --")
    for rec in state.get("recommendations", []):
        print(f"{rec['rank_label']}: {rec['name']} | ₹{rec['price']:,} | {rec['rating']}⭐ | "
              f"{rec['source']} | score={rec['recommendation_score']}")
        print(f"    breakdown: {rec['score_breakdown']}")
        print(f"    why: {rec['why']}")

    print(f"\nagent_status: {state['agent_status']}")
    if state.get("errors"):
        print(f"errors: {state['errors']}")


if __name__ == "__main__":
    base_state = {
        "query": "iPhone 15",
        "budget": 60000,
        "brand_filter": "",
        "products": [p.copy() for p in MOCK_PRODUCTS],
        "comparison_data": {},
        "recommendations": [],
        "agent_status": {"search": "completed", "comparison": "pending",
                          "recommendation": "pending", "response": "pending"},
        "errors": [],
    }
    run_case("CASE 1: No brand filter, budget 60,000", base_state)

    brand_state = {
        "query": "iPhone 15",
        "budget": 70000,
        "brand_filter": "Apple",
        "products": [p.copy() for p in MOCK_PRODUCTS],
        "comparison_data": {},
        "recommendations": [],
        "agent_status": {"search": "completed", "comparison": "pending",
                          "recommendation": "pending", "response": "pending"},
        "errors": [],
    }
    run_case("CASE 2: Brand filter = 'Apple', budget 70,000", brand_state)

    weighted_state = {
        "query": "iPhone 15",
        "budget": 0,
        "brand_filter": "",
        "weights": {"budget_fit": 5, "price": 10, "rating": 50, "reviews": 25, "value": 10},
        "products": [p.copy() for p in MOCK_PRODUCTS],
        "comparison_data": {},
        "recommendations": [],
        "agent_status": {"search": "completed", "comparison": "pending",
                          "recommendation": "pending", "response": "pending"},
        "errors": [],
    }
    run_case("CASE 3: Custom weights — user cares mostly about RATING, no budget set", weighted_state)

    print("\n\nAll cases ran without exceptions. ✅")
