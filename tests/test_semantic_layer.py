"""
Tests for Governed Semantic Engine: SQL compilation, dimension grouping, and parameterized execution.
"""

import pytest
from backend.app.semantic.layer import GovernedSemanticEngine
from backend.app.semantic.models import SemanticQueryRequest, FilterCondition


def test_semantic_query_revenue_by_region():
    req = SemanticQueryRequest(
        measures=["revenue", "profit", "margin_pct"],
        dimensions=["region"]
    )
    res = GovernedSemanticEngine.execute_query(req)
    assert res.status == "success"
    assert res.row_count == 5
    assert len(res.data) == 5
    for row in res.data:
        assert "region" in row
        assert "revenue" in row
        assert "profit" in row
        assert "margin_pct" in row
        assert row["revenue"] > 0


def test_semantic_query_product_leaderboard():
    req = SemanticQueryRequest(
        measures=["revenue"],
        dimensions=["product"],
        order_by="revenue",
        order_desc=True,
        limit=5
    )
    res = GovernedSemanticEngine.execute_query(req)
    assert res.status == "success"
    assert res.row_count == 5
    # Verify sorting descending
    revs = [r["revenue"] for r in res.data]
    assert revs == sorted(revs, reverse=True)


def test_semantic_query_with_filters():
    req = SemanticQueryRequest(
        measures=["revenue"],
        dimensions=["category"],
        filters=[FilterCondition(dimension="region", operator="=", value="Asia")]
    )
    res = GovernedSemanticEngine.execute_query(req)
    assert res.status == "success"
    assert res.row_count > 0


def test_semantic_query_invalid_measure_rejected():
    req = SemanticQueryRequest(
        measures=["non_existent_measure"]
    )
    res = GovernedSemanticEngine.execute_query(req)
    assert res.status == "error"
    assert res.governance_passed is False
    assert "Unknown metric" in res.error_message


def test_semantic_query_invalid_dimension_rejected():
    req = SemanticQueryRequest(
        measures=["revenue"],
        dimensions=["invalid_dimension"]
    )
    res = GovernedSemanticEngine.execute_query(req)
    assert res.status == "error"
    assert "Unknown dimension" in res.error_message
