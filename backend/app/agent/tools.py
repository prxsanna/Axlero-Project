"""
Governed Semantic Layer Tools for MetricMind.

Provides controlled, governed LangChain-compatible tools that the AI Agent invokes.
The Agent CANNOT execute raw SQL; it must call these approved semantic functions.
"""

from typing import List, Dict, Any, Optional
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field

from backend.app.semantic.metadata import METRICS_DICTIONARY, DIMENSIONS_DICTIONARY
from backend.app.semantic.models import SemanticQueryRequest, FilterCondition
from backend.app.semantic.layer import GovernedSemanticEngine

# ---------------------------------------------------------
# CATALOG TOOL
# ---------------------------------------------------------

@tool
def get_semantic_catalog() -> Dict[str, Any]:
    """
    Returns the authoritative catalog of governed business metrics and dimensions.
    """
    return {
        "measures": {
            k: {
                "name": v["name"],
                "label": v["label"],
                "description": v["description"],
                "unit": v["unit"],
                "format": v["format"]
            }
            for k, v in METRICS_DICTIONARY.items()
        },
        "dimensions": {
            k: {
                "name": v["name"],
                "label": v["label"],
                "type": v["type"]
            }
            for k, v in DIMENSIONS_DICTIONARY.items()
        }
    }


# ---------------------------------------------------------
# GOVERNED EXECUTION TOOL
# ---------------------------------------------------------

def execute_governed_query(
    measures: List[str],
    dimensions: Optional[List[str]] = None,
    filters: Optional[List[Dict[str, Any]]] = None,
    limit: Optional[int] = 100,
    order_by: Optional[str] = None,
    order_desc: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Executes a governed semantic query through Cube.dev / PostgreSQL and returns structured data.
    """
    filter_objs = []
    if filters:
        for f in filters:
            if isinstance(f, dict):
                filter_objs.append(FilterCondition(
                    dimension=f.get("dimension", ""),
                    operator=f.get("operator", "="),
                    value=f.get("value", "")
                ))
            elif isinstance(f, FilterCondition):
                filter_objs.append(f)

    req = SemanticQueryRequest(
        measures=measures,
        dimensions=dimensions or [],
        filters=filter_objs,
        limit=limit or 100,
        order_by=order_by,
        order_desc=order_desc if order_desc is not None else True
    )

    res = GovernedSemanticEngine.execute_query(req)
    return res.model_dump()


# ---------------------------------------------------------
# SPECIFIC METRIC TOOLS
# ---------------------------------------------------------

def get_revenue(
    region: Optional[str] = None,
    product: Optional[str] = None,
    category: Optional[str] = None,
    year: Optional[int] = None,
    quarter: Optional[str] = None,
    month: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves governed Revenue (total gross sales) with optional filters.
    """
    filters = []
    if region:
        filters.append({"dimension": "region", "operator": "=", "value": region})
    if product:
        filters.append({"dimension": "product", "operator": "=", "value": product})
    if category:
        filters.append({"dimension": "category", "operator": "=", "value": category})
    if year:
        filters.append({"dimension": "year", "operator": "=", "value": str(year)})
    if quarter:
        filters.append({"dimension": "quarter", "operator": "=", "value": quarter})
    if month:
        filters.append({"dimension": "month", "operator": "=", "value": month})

    return execute_governed_query(
        measures=["revenue"],
        filters=filters
    )


def get_cost(
    region: Optional[str] = None,
    product: Optional[str] = None,
    category: Optional[str] = None,
    year: Optional[int] = None,
    quarter: Optional[str] = None,
    month: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves governed Total Cost with optional filters.
    """
    filters = []
    if region:
        filters.append({"dimension": "region", "operator": "=", "value": region})
    if product:
        filters.append({"dimension": "product", "operator": "=", "value": product})
    if category:
        filters.append({"dimension": "category", "operator": "=", "value": category})
    if year:
        filters.append({"dimension": "year", "operator": "=", "value": str(year)})
    if quarter:
        filters.append({"dimension": "quarter", "operator": "=", "value": quarter})
    if month:
        filters.append({"dimension": "month", "operator": "=", "value": month})

    return execute_governed_query(
        measures=["cost"],
        filters=filters
    )


def get_profit(
    region: Optional[str] = None,
    product: Optional[str] = None,
    category: Optional[str] = None,
    year: Optional[int] = None,
    quarter: Optional[str] = None,
    month: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves governed Operating Profit (Revenue - Cost) with optional filters.
    """
    filters = []
    if region:
        filters.append({"dimension": "region", "operator": "=", "value": region})
    if product:
        filters.append({"dimension": "product", "operator": "=", "value": product})
    if category:
        filters.append({"dimension": "category", "operator": "=", "value": category})
    if year:
        filters.append({"dimension": "year", "operator": "=", "value": str(year)})
    if quarter:
        filters.append({"dimension": "quarter", "operator": "=", "value": quarter})
    if month:
        filters.append({"dimension": "month", "operator": "=", "value": month})

    return execute_governed_query(
        measures=["profit", "margin_pct"],
        filters=filters
    )


def get_margin(
    region: Optional[str] = None,
    product: Optional[str] = None,
    category: Optional[str] = None,
    year: Optional[int] = None,
    quarter: Optional[str] = None,
    month: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves governed Margin and Margin Percentage with optional filters.
    """
    filters = []
    if region:
        filters.append({"dimension": "region", "operator": "=", "value": region})
    if product:
        filters.append({"dimension": "product", "operator": "=", "value": product})
    if category:
        filters.append({"dimension": "category", "operator": "=", "value": category})
    if year:
        filters.append({"dimension": "year", "operator": "=", "value": str(year)})
    if quarter:
        filters.append({"dimension": "quarter", "operator": "=", "value": quarter})
    if month:
        filters.append({"dimension": "month", "operator": "=", "value": month})

    return execute_governed_query(
        measures=["margin", "margin_pct", "revenue", "cost"],
        filters=filters
    )


def get_sales_by_region(
    metric: str = "revenue",
    product: Optional[str] = None,
    category: Optional[str] = None,
    year: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieves metric breakdown across all sales regions.
    """
    if metric not in METRICS_DICTIONARY:
        metric = "revenue"

    filters = []
    if product:
        filters.append({"dimension": "product", "operator": "=", "value": product})
    if category:
        filters.append({"dimension": "category", "operator": "=", "value": category})
    if year:
        filters.append({"dimension": "year", "operator": "=", "value": str(year)})

    return execute_governed_query(
        measures=[metric],
        dimensions=["region"],
        filters=filters,
        limit=20
    )


def get_sales_by_product(
    metric: str = "revenue",
    region: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Retrieves product ranking and performance for a specified metric.
    """
    if metric not in METRICS_DICTIONARY:
        metric = "revenue"

    filters = []
    if region:
        filters.append({"dimension": "region", "operator": "=", "value": region})
    if category:
        filters.append({"dimension": "category", "operator": "=", "value": category})

    return execute_governed_query(
        measures=[metric],
        dimensions=["product"],
        filters=filters,
        limit=limit,
        order_by=metric,
        order_desc=True
    )


def get_customer_metrics(
    segment: Optional[str] = None,
    region: Optional[str] = None,
    churn_status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves customer count, revenue, and transaction statistics.
    """
    filters = []
    if segment:
        filters.append({"dimension": "customer_segment", "operator": "=", "value": segment})
    if region:
        filters.append({"dimension": "region", "operator": "=", "value": region})
    if churn_status:
        filters.append({"dimension": "churn_status", "operator": "=", "value": churn_status})

    return execute_governed_query(
        measures=["customer_count", "revenue", "quantity", "transaction_count"],
        filters=filters
    )


ALL_GOVERNED_TOOLS = [
    get_semantic_catalog,
    get_revenue,
    get_cost,
    get_profit,
    get_margin,
    get_sales_by_region,
    get_sales_by_product,
    get_customer_metrics,
    execute_governed_query
]
