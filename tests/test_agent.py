"""
Tests for LangChain + Gemini Conversational BI Agent.
"""

import pytest
from backend.app.agent.agent import MetricMindAgent

agent = MetricMindAgent()


def test_agent_total_revenue():
    res = agent.process_query("How much revenue did we make?")
    assert res["status"] == "success"
    assert "$" in res["answer"]
    assert res["metric"] == "revenue"
    assert res["transparency"]["total_rows_scanned"] > 0


def test_agent_europe_revenue():
    res = agent.process_query("How much revenue did we make in Europe?")
    assert res["status"] == "success"
    assert "$" in res["answer"]
    assert "Europe" in res["explanation"]


def test_agent_revenue_by_region():
    res = agent.process_query("Show revenue by region.")
    assert res["status"] == "success"
    assert res["chart_config"] is not None
    assert res["chart_config"]["series"][0]["type"] == "bar"


def test_agent_profit_query():
    res = agent.process_query("What is our profit?")
    assert res["status"] == "success"
    assert "$" in res["answer"]


def test_agent_margin_query():
    res = agent.process_query("What is our margin?")
    assert res["status"] == "success"


def test_agent_unsupported_metric_clarification():
    res = agent.process_query("How much happiness did we generate?")
    assert res["status"] == "clarification_needed"
    assert "Clarification Required" in res["answer"]
    assert res["chart_config"] is None


def test_agent_multi_step_root_cause():
    res = agent.process_query("Why did our European margins drop last quarter?")
    assert res["status"] == "success"
    assert len(res["reasoning_steps"]) >= 2
    assert res["chart_config"] is not None
    assert len(res["transparency"]["api_calls"]) >= 2
