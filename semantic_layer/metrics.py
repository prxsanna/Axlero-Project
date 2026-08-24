# MetricMind Semantic Layer
# This file contains the approved business metric definitions.

METRICS = {
    "revenue": {
        "name": "Revenue",
        "formula": "SUM(revenue)",
        "description": "Total revenue generated"
    },

    "cost": {
        "name": "Cost",
        "formula": "SUM(cost)",
        "description": "Total cost incurred"
    },

    "profit": {
        "name": "Profit",
        "formula": "Revenue - Cost",
        "description": "Total profit generated"
    },

    "margin": {
        "name": "Margin",
        "formula": "(Revenue - Cost) / Revenue",
        "description": "Profit as a percentage of revenue"
    }
}


def get_metric(metric_name):
    """
    Return the definition of an approved metric.
    """

    metric_name = metric_name.lower()

    if metric_name not in METRICS:
        raise ValueError(f"Metric '{metric_name}' is not approved.")

    return METRICS[metric_name]