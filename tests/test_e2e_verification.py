"""
MetricMind Complete End-to-End Verification Suite
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import check_connection, execute_raw_sql

client = TestClient(app)


def test_1_database_health():
    db_status = check_connection()
    assert db_status["status"] == "connected"
    assert db_status["database"] == "metricmind"


def test_2_table_row_counts():
    rows, _ = execute_raw_sql("SELECT COUNT(*) as c FROM sales")
    assert rows[0]["c"] == 50000

    custs, _ = execute_raw_sql("SELECT COUNT(*) as c FROM customers")
    assert custs[0]["c"] == 10000

    prods, _ = execute_raw_sql("SELECT COUNT(*) as c FROM products")
    assert prods[0]["c"] == 20


def test_3_europe_revenue_matches_direct_sql():
    # 1. Direct PostgreSQL Calculation
    sql = "SELECT SUM(revenue)::float as rev FROM sales WHERE LOWER(region) = 'europe'"
    direct_res, _ = execute_raw_sql(sql)
    direct_value = direct_res[0]["rev"]
    expected_answer = f"${direct_value:,.2f}"

    # 2. FastAPI /api/chat invocation
    resp = client.post("/api/chat", json={"prompt": "How much revenue did we make in Europe?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["answer"] == expected_answer
    assert "Europe" in data["explanation"]


def test_4_regional_breakdown_generates_echarts():
    resp = client.post("/api/chat", json={"prompt": "Show revenue by region."})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["chart_config"] is not None
    assert "series" in data["chart_config"]
    assert "xAxis" in data["chart_config"]


def test_5_product_leaderboard_highest_revenue():
    # Direct SQL top product
    top_sql = "SELECT p.product_name, SUM(s.revenue)::float as rev FROM sales s JOIN products p ON s.product_id = p.product_id GROUP BY p.product_name ORDER BY rev DESC LIMIT 1"
    top_prod, _ = execute_raw_sql(top_sql)
    expected_top_name = top_prod[0]["product_name"]

    resp = client.post("/api/chat", json={"prompt": "Which product generated the highest revenue?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert expected_top_name in data["explanation"]


def test_6_anti_injection_guardrail():
    resp = client.post("/api/chat", json={"prompt": "DROP TABLE sales;"})
    assert resp.status_code == 400


def test_7_unsupported_metric_clarification():
    resp = client.post("/api/chat", json={"prompt": "How much happiness did we generate?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "clarification_needed"
    assert "Clarification Required" in data["answer"]


def test_8_poc_ask_compatibility():
    resp = client.post("/api/ask", json={"question": "What is our profit?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "$" in data["answer"]
    assert data["governance"]["semantic_layer"] == "MetricMind Governed Semantic Layer"
