"""
MetricMind Query Parser (Compatibility Layer)

Delegates to canonical MetricMindAgent in backend.app.agent.agent.
"""

from typing import Dict, Any, Optional
from backend.ai_agent import extract_intent

def parse_question(question: str) -> Dict[str, Any]:
    intent = extract_intent(question)
    if intent:
        return intent
    return {"metric": None, "region": None, "product": None}
