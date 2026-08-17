"""
MetricMind Semantic Layer

This file contains the official definitions of business metrics.

IMPORTANT:
The AI should NOT invent these formulas.

The Semantic Layer is the single source of truth.
"""

METRICS = {
    "revenue": {
        "name": "Revenue",
        "definition": "Total revenue generated from sales.",
        "formula": "SUM(revenue)",
        "column": "revenue",
        "type": "sum"
    },

    "cost": {
        "name": "Cost",
        "definition": "Total cost associated with sales.",
        "formula": "SUM(cost)",
        "column": "cost",
        "type": "sum"
    },

    "profit": {
        "name": "Profit",
        "definition": "Revenue minus cost.",
        "formula": "Revenue - Cost",
        "type": "calculated"
    },

    "margin": {
        "name": "Margin",
        "definition": "Profit divided by revenue.",
        "formula": "(Revenue - Cost) / Revenue",
        "type": "calculated"
    }
}


DIMENSIONS = {
    "region": {
        "name": "Region",
        "column": "region",
        "values": [
            "Europe",
            "Asia",
            "North America"
        ]
    },

    "product": {
        "name": "Product",
        "column": "product",
        "values": [
            "Software",
            "Hardware",
            "Services"
        ]
    },

    "date": {
        "name": "Date",
        "column": "date"
    }
}


def get_metric(metric_name: str):
    """
    Return a metric definition.
    """

    metric_name = metric_name.lower().strip()

    if metric_name not in METRICS:
        return None

    return METRICS[metric_name]


def get_available_metrics():
    """
    Return all metrics available to MetricMind.
    """

    return METRICS


def get_available_dimensions():
    """
    Return all dimensions available to MetricMind.
    """

    return DIMENSIONS