"""
Comparison Agent — Member 4

Responsibility: take the raw product list produced by the Search Agent
(Amazon + Flipkart + Firecrawl, merged) and turn it into structured
comparison intelligence: cheapest, highest rated, best value, price/rating
stats, grouping by source and brand, and outlier flags.

Input state keys read:
    products        : List[Dict]  (from Search Agent)
    brand_filter     : str         (optional, from UI)

Output state keys written:
    products         : List[Dict]  (brand-filtered — see note below)
    comparison_data  : Dict
    agent_status      : Dict
    errors           : List[str]

IMPORTANT — brand_filter contract:
    brand_filter was previously wired into the UI and workflow state but
    never actually applied anywhere in the pipeline. This agent is where
    filtering now happens: products are filtered by brand BEFORE any stats
    are computed, and the FILTERED list is written back to state['products']
    so the Recommendation Agent and Response Agent downstream only ever see
    matching products. Flag this design choice to whoever owns the LangGraph
    state schema (Member 1) and the UI (Member 5) so everyone's expectations
    line up.
"""

from typing import Any, Dict, List

from utils.logger import setup_logger
from utils.helpers import calculate_value_score, brand_matches, detect_price_outliers
from utils.constants import OUTLIER_STD_THRESHOLD

logger = setup_logger("ComparisonAgent")


def comparison_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """Compares products across price, rating, brand, and specs."""
    products = state.get("products", [])
    brand_filter = state.get("brand_filter", "") or ""
    agent_status = state.get("agent_status", {}).copy()
    agent_status["comparison"] = "running"
    errors = state.get("errors", []).copy()

    logger.info(f"Comparison Agent started with {len(products)} products, brand_filter='{brand_filter}'")

    # --- Apply brand filter early, before any stats are computed ---
    if brand_filter:
        before = len(products)
        products = [p for p in products if brand_matches(p.get("brand", ""), brand_filter)]
        logger.info(f"Brand filter '{brand_filter}' matched {len(products)}/{before} products")

    if not products:
        logger.warning("No products to compare (empty list or brand filter matched nothing)")
        agent_status["comparison"] = "completed"
        return {
            "products": products,
            "comparison_data": {},
            "agent_status": agent_status,
            "errors": errors,
        }

    try:
        priced = [p for p in products if p.get("price", 0) > 0]
        rated = [p for p in products if p.get("rating", 0) > 0]

        cheapest = min(priced, key=lambda x: x["price"]) if priced else None
        highest_rated = max(rated, key=lambda x: x["rating"]) if rated else None

        # Value score per product (rating vs price tradeoff, 0-100)
        max_price = max((p["price"] for p in priced), default=1) or 1
        for p in products:
            p["value_score"] = calculate_value_score(p.get("price", 0), p.get("rating", 0), max_price)

        valued = [p for p in products if p.get("value_score", 0) > 0]
        best_value = max(valued, key=lambda x: x["value_score"]) if valued else None

        # Group by source / brand
        by_source: Dict[str, List[Dict]] = {}
        for p in products:
            by_source.setdefault(p.get("source", "Unknown"), []).append(p)

        by_brand: Dict[str, List[Dict]] = {}
        for p in products:
            by_brand.setdefault(p.get("brand", "Unknown") or "Unknown", []).append(p)

        # Price / rating stats
        prices = [p["price"] for p in priced]
        price_stats = {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0,
            "avg": sum(prices) / len(prices) if prices else 0,
        }

        ratings = [p["rating"] for p in rated]
        rating_stats = {
            "min": min(ratings) if ratings else 0,
            "max": max(ratings) if ratings else 0,
            "avg": sum(ratings) / len(ratings) if ratings else 0,
        }

        # Outlier detection — likely scraping/matching errors worth flagging in UI
        outliers = detect_price_outliers(products, OUTLIER_STD_THRESHOLD)
        if outliers:
            logger.warning(f"Flagged {len(outliers)} price outlier(s): "
                            f"{[o.get('name') for o in outliers]}")

        comparison_data = {
            "cheapest": cheapest,
            "highest_rated": highest_rated,
            "best_value": best_value,
            "by_source": by_source,
            "by_brand": by_brand,
            "price_stats": price_stats,
            "rating_stats": rating_stats,
            "total_products": len(products),
            "outliers": outliers,
            "brand_filter_applied": bool(brand_filter),
        }

        agent_status["comparison"] = "completed"
        logger.info("Comparison Agent completed successfully")

        return {
            "products": products,
            "comparison_data": comparison_data,
            "agent_status": agent_status,
            "errors": errors,
        }

    except Exception as e:
        logger.error(f"Comparison Agent failed: {e}")
        errors.append(f"Comparison failed: {str(e)}")
        agent_status["comparison"] = "failed"
        return {
            "products": products,
            "comparison_data": {},
            "agent_status": agent_status,
            "errors": errors,
        }
