"""
MetricMind Semantic Engine

This module is responsible for executing governed metrics.

The AI does NOT directly access the CSV.

The AI asks the Semantic Engine for a metric.

Example:

{
    "metric": "revenue",
    "region": "Europe"
}

The Semantic Engine performs the actual calculation.
"""

import os
import pandas as pd

from semantic_layer.metrics import (
    get_metric,
    get_available_metrics,
    get_available_dimensions
)


# ---------------------------------------------------------
# FIND DATA FILE
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sales.csv"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

def apply_filters(
    data,
    region=None,
    product=None,
    start_date=None,
    end_date=None
):
    """
    Apply approved filters to the business dataset.
    """

    filtered = data.copy()

    if region:
        filtered = filtered[
            filtered["region"].str.lower() == region.lower()
        ]

    if product:
        filtered = filtered[
            filtered["product"].str.lower() == product.lower()
        ]

    if start_date:
        filtered = filtered[
            filtered["date"] >= pd.to_datetime(start_date)
        ]

    if end_date:
        filtered = filtered[
            filtered["date"] <= pd.to_datetime(end_date)
        ]

    return filtered


# ---------------------------------------------------------
# CALCULATE METRIC
# ---------------------------------------------------------

def calculate_metric(
    metric,
    region=None,
    product=None,
    start_date=None,
    end_date=None
):
    """
    Calculate a governed MetricMind metric.

    Supported metrics:

    revenue
    cost
    profit
    margin
    """

    metric = metric.lower().strip()

    # Check that the metric is officially defined.
    metric_definition = get_metric(metric)

    if not metric_definition:
        raise ValueError(
            f"Metric '{metric}' is not available "
            f"in the MetricMind Semantic Layer."
        )

    # Apply filters.
    filtered = apply_filters(
        df,
        region=region,
        product=product,
        start_date=start_date,
        end_date=end_date
    )

    # Prevent invalid empty queries.
    if filtered.empty:
        raise ValueError(
            "No data was found for the requested filters."
        )

    # -----------------------------------------------------
    # REVENUE
    # -----------------------------------------------------

    if metric == "revenue":

        value = filtered["revenue"].sum()

    # -----------------------------------------------------
    # COST
    # -----------------------------------------------------

    elif metric == "cost":

        value = filtered["cost"].sum()

    # -----------------------------------------------------
    # PROFIT
    # -----------------------------------------------------

    elif metric == "profit":

        revenue = filtered["revenue"].sum()
        cost = filtered["cost"].sum()

        value = revenue - cost

    # -----------------------------------------------------
    # MARGIN
    # -----------------------------------------------------

    elif metric == "margin":

        revenue = filtered["revenue"].sum()
        cost = filtered["cost"].sum()

        if revenue == 0:
            value = 0

        else:
            value = (revenue - cost) / revenue

    else:

        raise ValueError(
            f"Metric '{metric}' is not implemented."
        )

    return {
        "metric": metric_definition["name"],
        "definition": metric_definition["definition"],
        "formula": metric_definition["formula"],
        "value": float(value),
        "rows_used": len(filtered),

        "filters": {
            "region": region,
            "product": product,
            "start_date": start_date,
            "end_date": end_date
        }
    }


# ---------------------------------------------------------
# GET DATASET SUMMARY
# ---------------------------------------------------------

def get_dataset_summary():

    return {
        "rows": len(df),
        "regions": sorted(
            df["region"].unique().tolist()
        ),
        "products": sorted(
            df["product"].unique().tolist()
        ),
        "metrics": list(
            get_available_metrics().keys()
        ),
        "dimensions": list(
            get_available_dimensions().keys()
        )
    }