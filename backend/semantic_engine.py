"""
MetricMind Semantic Engine

This module is responsible for executing governed metrics against PostgreSQL.
It provides backward-compatible helper functions while routing through the
authoritative GovernedSemanticEngine.
"""

from typing import Optional, Dict, Any
from backend.app.semantic.layer import GovernedSemanticEngine
from backend.app.semantic.models import SemanticQueryRequest, FilterCondition
from backend.app.semantic.metadata import METRICS_DICTIONARY, DIMENSIONS_DICTIONARY
from backend.database import execute_raw_sql


def calculate_metric(
    metric: str,
    region: Optional[str] = None,
    product: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate a governed MetricMind metric against PostgreSQL.
    """
    metric_clean = metric.lower().strip()
    if metric_clean not in METRICS_DICTIONARY:
        raise ValueError(
            f"Metric '{metric}' is not available in the MetricMind Semantic Layer."
        )

    filters = []
    if region:
        filters.append(FilterCondition(dimension="region", operator="=", value=region))
    if product:
        filters.append(FilterCondition(dimension="product", operator="=", value=product))
    if start_date:
        filters.append(FilterCondition(dimension="date", operator=">=", value=start_date))
    if end_date:
        filters.append(FilterCondition(dimension="date", operator="<=", value=end_date))

    req = SemanticQueryRequest(
        measures=[metric_clean],
        filters=filters
    )

    res = GovernedSemanticEngine.execute_query(req)

    if res.status != "success" or not res.data:
        raise ValueError(res.error_message or "No data was found for the requested filters.")

    val = res.data[0].get(metric_clean, 0.0)
    meta = METRICS_DICTIONARY[metric_clean]

    return {
        "metric": meta["label"],
        "definition": meta["description"],
        "formula": meta["sql_formula"],
        "value": float(val),
        "rows_used": res.row_count,
        "filters": {
            "region": region,
            "product": product,
            "start_date": start_date,
            "end_date": end_date
        }
    }


def get_dataset_summary() -> Dict[str, Any]:
    """
    Returns summary metadata from the live PostgreSQL database.
    """
    rows_count, _ = execute_raw_sql("SELECT COUNT(*) as cnt FROM sales")
    regions_rows, _ = execute_raw_sql("SELECT DISTINCT region FROM sales ORDER BY region")
    products_rows, _ = execute_raw_sql("SELECT DISTINCT product_name FROM products ORDER BY product_name")

    return {
        "rows": rows_count[0]["cnt"] if rows_count else 0,
        "regions": [r["region"] for r in regions_rows],
        "products": [p["product_name"] for p in products_rows],
        "metrics": list(METRICS_DICTIONARY.keys()),
        "dimensions": list(DIMENSIONS_DICTIONARY.keys())
    }
