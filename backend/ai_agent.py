"""
MetricMind Gemini AI Agent

Understands natural language questions and extracts controlled intents.
Integrates with LangChain and Google Gemini for governed BI reasoning.
"""

import os
from typing import Optional, Dict, Any
from backend.app.agent.agent import MetricMindAgent

_agent = MetricMindAgent()

ALLOWED_METRICS = [
    "revenue",
    "cost",
    "profit",
    "margin",
    "margin_pct",
    "quantity"
]

ALLOWED_REGIONS = [
    "Asia",
    "Europe",
    "North America",
    "Oceania",
    "South America"
]

def extract_intent(question: str) -> Optional[Dict[str, Any]]:
    """
    Extracts a governed intent from the natural language question.
    """
    if not question or not question.strip():
        return None

    reasoning_steps = []
    intent = _agent._resolve_intent_with_gemini(question, reasoning_steps)

    measures = intent.get("measures", [])
    metric = measures[0] if measures else None
    
    region = None
    for f in intent.get("filters", []):
        if f.get("dimension") == "region":
            region = f.get("value")

    product = None
    for f in intent.get("filters", []):
        if f.get("dimension") == "product":
            product = f.get("value")

    return {
        "metric": metric,
        "region": region,
        "product": product
    }