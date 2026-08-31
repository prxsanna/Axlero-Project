"""
Tests for MetricMind Governance Guardrails & Anti-Injection Protection.
"""

import pytest
from backend.app.core.governance import GovernanceGuardrails, PromptInjectionError


def test_drop_table_blocked():
    with pytest.raises(PromptInjectionError, match="Security Safeguard Triggered"):
        GovernanceGuardrails.inspect_prompt_safety("DROP TABLE sales;")


def test_delete_from_blocked():
    with pytest.raises(PromptInjectionError, match="Security Safeguard Triggered"):
        GovernanceGuardrails.inspect_prompt_safety("DELETE FROM customers WHERE id = 1")


def test_sql_semicolon_injection_blocked():
    with pytest.raises(PromptInjectionError, match="Security Safeguard Triggered"):
        GovernanceGuardrails.inspect_prompt_safety("Show revenue; SELECT * FROM pg_user")


def test_truncate_table_blocked():
    with pytest.raises(PromptInjectionError, match="Security Safeguard Triggered"):
        GovernanceGuardrails.inspect_prompt_safety("TRUNCATE TABLE products")


def test_benign_business_question_allowed():
    # Should not raise any error
    GovernanceGuardrails.inspect_prompt_safety("How much revenue did we make in Europe?")
    GovernanceGuardrails.inspect_prompt_safety("Show profit and cost by region.")


def test_step_limit_enforced():
    with pytest.raises(Exception, match="Governance Limit Exceeded"):
        GovernanceGuardrails.enforce_step_limit(current_step=6, max_steps=5)
