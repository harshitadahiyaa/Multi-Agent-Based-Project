"""
Shared data contract for the Product Price Comparison Assistant.

NOTE FOR TEAM: This file defines the `Product` schema that EVERY agent/service
in the pipeline reads and writes. It currently lives here because Member 4's
(Comparison + Recommendation) agents cannot be written or tested without it,
and no shared utils existed yet in the repo.

Whoever owns Search Agent / Amazon / Flipkart / Firecrawl services should make
sure their code returns dicts that match this schema exactly (same field
names, same types). If a field needs to change, please discuss in the group
first since Comparison, Recommendation, and Response agents all depend on it.
"""

from pydantic import BaseModel, Field, field_validator


class Product(BaseModel):
    """Unified product data model used across all agents and services."""

    name: str = Field(default="Unknown Product", description="Product name")
    price: float = Field(default=0.0, description="Product price as float")
    rating: float = Field(default=0.0, description="Product rating 0-5")
    reviews: int = Field(default=0, description="Number of reviews")
    seller: str = Field(default="Unknown", description="Seller name")
    url: str = Field(default="", description="Product URL")
    image_url: str = Field(default="", description="Product image URL")
    source: str = Field(default="Unknown", description="Source platform e.g. Amazon, Flipkart")
    delivery_info: str = Field(default="", description="Delivery information")
    specifications: str = Field(default="", description="Product specifications")
    brand: str = Field(default="", description="Product brand")

    @field_validator("rating", mode="before")
    @classmethod
    def clamp_rating(cls, v):
        try:
            return max(0.0, min(5.0, float(v)))
        except (ValueError, TypeError):
            return 0.0

    @field_validator("price", mode="before")
    @classmethod
    def ensure_positive_price(cls, v):
        try:
            return max(0.0, float(v))
        except (ValueError, TypeError):
            return 0.0


def validate_search_query(query: str) -> str:
    """Validate and sanitize search query."""
    if not query:
        raise ValueError("Search query cannot be empty")

    cleaned = query.strip()
    if len(cleaned) < 2:
        raise ValueError("Search query must be at least 2 characters long")
    if len(cleaned) > 200:
        raise ValueError("Search query must be less than 200 characters")

    return cleaned


def validate_budget(budget: float) -> float:
    """Validate budget is non-negative."""
    try:
        val = float(budget)
        if val < 0:
            raise ValueError("Budget cannot be negative")
        return val
    except (ValueError, TypeError):
        raise ValueError("Invalid budget value")


def validate_weights(weights: dict) -> dict:
    """Validate recommendation scoring weights sum to (roughly) 100 and are non-negative.

    Falls back to defaults if invalid so a bad UI input never crashes the pipeline.
    """
    from utils.constants import DEFAULT_WEIGHTS

    if not weights or not isinstance(weights, dict):
        return DEFAULT_WEIGHTS.copy()

    try:
        cleaned = {k: max(0.0, float(v)) for k, v in weights.items()}
        total = sum(cleaned.values())
        if total <= 0:
            return DEFAULT_WEIGHTS.copy()
        # Normalize so components always sum to 100, regardless of what UI sends
        return {k: (v / total) * 100 for k, v in cleaned.items()}
    except (ValueError, TypeError):
        return DEFAULT_WEIGHTS.copy()
