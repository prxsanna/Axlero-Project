"""
MetricMind Semantic Layer (Compatibility Re-export)

Authoritative definitions are governed in backend.app.semantic.metadata.
"""

from backend.app.semantic.metadata import METRICS_DICTIONARY as METRICS, DIMENSIONS_DICTIONARY as DIMENSIONS

def get_metric(metric_name: str):
    metric_name = metric_name.lower().strip()
    return METRICS.get(metric_name)

def get_available_metrics():
    return METRICS

def get_available_dimensions():
    return DIMENSIONS
