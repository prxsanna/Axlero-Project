"""
Tests for MetricMind Governed Metrics and Calculations against PostgreSQL.
"""

import pytest
from backend.semantic_engine import calculate_metric, get_dataset_summary
from backend.app.semantic.metadata import METRICS_DICTIONARY


def test_get_dataset_summary():
    summary = get_dataset_summary()
    assert summary["rows"] == 50000
    assert "Asia" in summary["regions"]
    assert "Europe" in summary["regions"]
    assert "North America" in summary["regions"]
    assert len(summary["products"]) == 20


def test_calculate_revenue_total():
    result = calculate_metric("revenue")
    assert result["metric"] == "Revenue"
    assert result["value"] > 0
    assert result["rows_used"] >= 1


def test_calculate_revenue_filtered():
    result = calculate_metric("revenue", region="Europe")
    assert result["value"] > 0
    assert result["filters"]["region"] == "Europe"


def test_calculate_cost():
    result = calculate_metric("cost")
    assert result["metric"] == "Total Cost"
    assert result["value"] > 0


def test_calculate_profit_and_margin():
    rev_res = calculate_metric("revenue")
    cost_res = calculate_metric("cost")
    profit_res = calculate_metric("profit")

    # Verify arithmetic consistency: Profit == Revenue - Cost
    assert round(profit_res["value"], 2) == round(rev_res["value"] - cost_res["value"], 2)


def test_unsupported_metric_raises_error():
    with pytest.raises(ValueError, match="is not available"):
        calculate_metric("happiness_index")