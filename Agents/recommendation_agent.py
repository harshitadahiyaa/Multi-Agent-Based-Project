"""
Recommendation Agent — Member 4

Responsibility: take products + comparison_data (from the Comparison Agent)
and produce a ranked, personalized top-5 with a transparent score breakdown
per product.

Input state keys read:
    products         : List[Dict]  (already brand-filtered by Comparison Agent)
    budget           : float
    comparison_data   : Dict        (for value_score per product)
    weights          : Dict         (optional, from UI sliders — see utils.constants.DEFAULT_WEIGHTS)

Output state keys written:
    recommendations  : List[Dict]   (top 5, ranked, each with 'score_breakdown' and 'why')
    agent_status      : Dict
    errors           : List[str]

Scoring (out of 100, weights configurable via state['weights']):
    - Budget fit   : within budget = full weight, within 10% over = half weight, else 0
    - Price        : (1 - price/max_price) * weight   (cheaper = better)
    - Rating       : (rating/5.0) * weight
    - Reviews      : log10(reviews+1), scaled and capped at weight
    - Value score  : (value_score/100) * weight        (comes from Comparison Agent)

Also diversifies the top-5 so it isn't dominated by one source, and attaches
a short human-readable "why" string per product built from its own score
breakdown (no LLM call needed — Response Agent can still layer Gemini on
top of this for the final narrative).
"""

import math
from typing import Any, Dict, List

from utils.logger import setup_logger
from utils.validators import validate_weights
from utils.constants import RANK_LABELS, MAX_PER_SOURCE_IN_TOP5

logger = setup_logger("RecommendationAgent")


def _score_product(product: Dict, budget: float, max_price: float, weights: Dict) -> Dict:
    """Compute weighted score + a breakdown dict for a single product."""
    price = product.get("price", 0)
    rating = product.get("rating", 0)
    reviews = product.get("reviews", 0)
    value_score = product.get("value_score", 0)

    breakdown = {}

    # Budget fit
    budget_pts = 0.0
    if budget > 0:
        if price <= budget:
            budget_pts = weights["budget_fit"]
        elif price <= budget * 1.1:
            budget_pts = weights["budget_fit"] * 0.5
    else:
        budget_pts = weights["budget_fit"] * 0.33  # small neutral credit when no budget set
    breakdown["budget_fit"] = round(budget_pts, 2)

    # Price (cheaper = better)
    price_pts = 0.0
    if max_price > 0 and price > 0:
        price_pts = (1 - price / max_price) * weights["price"]
    breakdown["price"] = round(price_pts, 2)

    # Rating
    rating_pts = (rating / 5.0) * weights["rating"] if rating > 0 else 0.0
    breakdown["rating"] = round(rating_pts, 2)

    # Reviews (log-scaled, capped at the weight)
    reviews_pts = 0.0
    if reviews > 0:
        reviews_pts = min(math.log10(reviews + 1) * (weights["reviews"] / 3), weights["reviews"])
    breakdown["reviews"] = round(reviews_pts, 2)

    # Value score bonus (from Comparison Agent)
    value_pts = (value_score / 100) * weights["value"] if value_score else 0.0
    breakdown["value"] = round(value_pts, 2)

    total = round(sum(breakdown.values()), 2)
    return {"score": total, "breakdown": breakdown}


def _why_text(product: Dict, breakdown: Dict, budget: float) -> str:
    """Build a short, human-readable reason string from the score breakdown."""
    reasons = []
    top_factor = max(breakdown, key=breakdown.get)

    if budget > 0 and product.get("price", 0) <= budget:
        reasons.append("fits your budget")
    if breakdown.get("rating", 0) >= breakdown.get("price", 0) and product.get("rating", 0) >= 4.0:
        reasons.append(f"highly rated ({product.get('rating')}\u2b50)")
    if top_factor == "price" and breakdown["price"] > 15:
        reasons.append("one of the cheapest options")
    if top_factor == "value":
        reasons.append("strong price-to-rating value")
    if product.get("reviews", 0) > 1000:
        reasons.append(f"backed by {product.get('reviews'):,} reviews")

    if not reasons:
        reasons.append("balanced across price, rating and reviews")

    return "Recommended because it's " + ", ".join(reasons[:3]) + "."


def _diversify(scored_products: List[Dict], top_n: int = 5, max_per_source: int = MAX_PER_SOURCE_IN_TOP5) -> List[Dict]:
    """Pick top_n products by score, but cap how many can come from a single
    source so the list isn't just 5 near-duplicate Amazon listings.
    """
    result = []
    source_counts: Dict[str, int] = {}

    for product in scored_products:
        src = product.get("source", "Unknown")
        if source_counts.get(src, 0) >= max_per_source:
            continue
        result.append(product)
        source_counts[src] = source_counts.get(src, 0) + 1
        if len(result) == top_n:
            break

    # Backfill if diversification left us short (e.g. only 2 sources total)
    if len(result) < top_n:
        for product in scored_products:
            if product not in result:
                result.append(product)
            if len(result) == top_n:
                break

    return result


def recommendation_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """Ranks products based on budget, ratings, reviews, and value — with
    configurable weights and a transparent per-product score breakdown."""
    products = state.get("products", [])
    budget = state.get("budget", 0) or 0
    weights = validate_weights(state.get("weights", {}))
    comparison_data = state.get("comparison_data", {})
    agent_status = state.get("agent_status", {}).copy()
    agent_status["recommendation"] = "running"
    errors = state.get("errors", []).copy()

    logger.info(f"Recommendation Agent started with {len(products)} products, budget={budget}, weights={weights}")

    if not products:
        logger.warning("No products to recommend")
        agent_status["recommendation"] = "completed"
        return {"recommendations": [], "agent_status": agent_status, "errors": errors}

    try:
        # Exclude price outliers flagged by the Comparison Agent (likely scraping
        # errors or mismatched products, e.g. a ₹4,999 "iPhone 15") from
        # eligibility for recommendation, even though they're still shown in
        # comparison_data for transparency.
        outlier_urls = {o.get("url") for o in comparison_data.get("outliers", []) if o.get("url")}
        eligible_products = [p for p in products if p.get("url") not in outlier_urls] if outlier_urls else products
        if outlier_urls:
            logger.info(f"Excluded {len(products) - len(eligible_products)} outlier product(s) from recommendations")

        if not eligible_products:
            logger.warning("All products were flagged as outliers; falling back to full list")
            eligible_products = products

        max_price = max((p.get("price", 0) for p in eligible_products), default=0) or 1

        scored_products = []
        for product in eligible_products:
            result = _score_product(product, budget, max_price, weights)
            enriched = product.copy()
            enriched["recommendation_score"] = result["score"]
            enriched["score_breakdown"] = result["breakdown"]
            enriched["why"] = _why_text(product, result["breakdown"], budget)
            scored_products.append(enriched)

        scored_products.sort(key=lambda x: x["recommendation_score"], reverse=True)

        recommendations = _diversify(scored_products, top_n=5)

        for i, rec in enumerate(recommendations):
            rec["rank"] = i + 1
            rec["rank_label"] = RANK_LABELS[i] if i < len(RANK_LABELS) else f"{i + 1}th Choice"

        agent_status["recommendation"] = "completed"
        top_score = recommendations[0]["recommendation_score"] if recommendations else 0
        logger.info(f"Recommendation Agent ranked {len(scored_products)} products, top score: {top_score}")

        return {
            "recommendations": recommendations,
            "agent_status": agent_status,
            "errors": errors,
        }

    except Exception as e:
        logger.error(f"Recommendation Agent failed: {e}")
        errors.append(f"Recommendation failed: {str(e)}")
        agent_status["recommendation"] = "failed"
        return {"recommendations": [], "agent_status": agent_status, "errors": errors}
