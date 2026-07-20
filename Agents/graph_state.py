"""
Shared LangGraph state — Member 1

Mirrors the state dict contract that Agents/comparison_agent.py and
Agents/recommendation_agent.py already depend on (see their docstrings),
plus the query/products/final_response fields the Search and Response
agents add.
"""
from typing import TypedDict, List, Dict, Any


class ProductComparisonState(TypedDict, total=False):
    # ---- input from the UI ----
    query: str
    budget: float
    brand_filter: str
    weights: Dict[str, float]

    # ---- filled by Search Agent ----
    products: List[Dict[str, Any]]

    # ---- filled by Comparison Agent (Member 4) ----
    comparison_data: Dict[str, Any]

    # ---- filled by Recommendation Agent (Member 4) ----
    recommendations: List[Dict[str, Any]]

    # ---- filled by Response Agent ----
    final_response: str

    # ---- shared / updated by every node ----
    agent_status: Dict[str, str]
    errors: List[str]
