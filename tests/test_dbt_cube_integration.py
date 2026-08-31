"""
Tests for MetricMind dbt Analytical Marts, Cube.dev Query Translation, and LangChain Governed Tools.
"""

import pytest
from backend.database import execute_raw_sql, verify_dbt_models, get_engine
from backend.app.semantic.layer import GovernedSemanticEngine
from backend.app.semantic.models import SemanticQueryRequest, FilterCondition
from backend.app.semantic.metadata import METRICS_DICTIONARY, DIMENSIONS_DICTIONARY
from backend.app.agent.tools import (
    get_revenue,
    get_cost,
    get_profit,
    get_margin,
    get_sales_by_region,
    get_sales_by_product,
    get_customer_metrics,
    get_semantic_catalog,
    execute_governed_query
)


def test_dbt_marts_created_and_populated():
    """Verify that all dbt staging views and analytical marts exist with 50,000 sales records."""
    assert verify_dbt_models(get_engine()) is True

    res, _ = execute_raw_sql("SELECT COUNT(*) as c FROM fct_sales")
    assert res[0]["c"] == 50000

    prods, _ = execute_raw_sql("SELECT COUNT(*) as c FROM dim_products")
    assert prods[0]["c"] == 20

    custs, _ = execute_raw_sql("SELECT COUNT(*) as c FROM dim_customers")
    assert custs[0]["c"] == 10000


def test_dbt_fct_sales_columns_match_governed_dimensions():
    """Verify that fct_sales contains all necessary analytical measures and dimensions."""
    res, _ = execute_raw_sql("SELECT * FROM fct_sales LIMIT 1")
    row = res[0]
    required_cols = [
        "sale_id", "order_id", "sale_date", "year", "quarter", "month",
        "customer_id", "customer_name", "country", "region", "customer_segment",
        "acquisition_channel", "product_id", "product", "category", "tier",
        "quantity", "revenue", "cost", "profit", "margin", "margin_pct",
        "material_cost", "shipping_cost"
    ]
    for col in required_cols:
        assert col in row, f"Column '{col}' missing from dbt mart fct_sales"


def test_cube_query_translation():
    """Verify that MetricMind semantic requests compile into valid Cube.dev REST query format."""
    req = SemanticQueryRequest(
        measures=["revenue", "margin_pct"],
        dimensions=["region", "quarter"],
        filters=[FilterCondition(dimension="category", operator="=", value="Analytics")],
        order_by="revenue",
        order_desc=True,
        limit=10
    )
    cube_q = GovernedSemanticEngine.build_cube_query(req)
    assert "query" in cube_q
    q = cube_q["query"]
    assert q["measures"] == ["sales.revenue", "sales.margin_pct"]
    assert q["dimensions"] == ["sales.region", "sales.quarter"]
    assert len(q["filters"]) == 1
    assert q["filters"][0]["member"] == "sales.category"
    assert q["filters"][0]["operator"] == "equals"
    assert q["filters"][0]["values"] == ["Analytics"]
    assert q["order"] == {"sales.revenue": "desc"}
    assert q["limit"] == 10


def test_cube_live_query_or_governed_fallback():
    """Verify that execute_query attempts Cube REST API and falls back to PostgreSQL fct_sales."""
    req = SemanticQueryRequest(
        measures=["revenue"],
        dimensions=["region"],
        limit=5
    )
    resp = GovernedSemanticEngine.execute_query(req)
    assert resp.status == "success"
    assert resp.governance_passed is True
    assert len(resp.data) == 5
    assert resp.data_source in [
        "Cube.dev Semantic Layer (sales_analytics)",
        "Governed Semantic Layer (PostgreSQL / fct_sales)"
    ]


def test_langchain_governed_tools_execution():
    """Verify that all governed LangChain tools execute through the semantic engine."""
    # 1. Catalog tool
    catalog = get_semantic_catalog.invoke({})
    assert "measures" in catalog
    assert "revenue" in catalog["measures"]

    # 2. Revenue tool with filter
    rev_res = get_revenue(region="Europe")
    assert rev_res["status"] == "success"
    assert rev_res["data"][0]["revenue"] == pytest.approx(9809305.67, 0.01)

    # 3. Regional breakdown tool
    reg_res = get_sales_by_region(metric="revenue")
    assert reg_res["status"] == "success"
    assert len(reg_res["data"]) == 5

    # 4. Product ranking tool
    prod_res = get_sales_by_product(metric="revenue", limit=5)
    assert prod_res["status"] == "success"
    assert len(prod_res["data"]) == 5
    assert prod_res["data"][0]["revenue"] >= prod_res["data"][1]["revenue"]

    # 5. Customer metrics tool
    cust_res = get_customer_metrics(segment="Enterprise")
    assert cust_res["status"] == "success"
    assert cust_res["data"][0]["customer_count"] > 0
