
import pandas as pd
from pathlib import Path
import sys

# Find the main MetricMind project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Allow Python to find the semantic_layer folder
sys.path.append(str(BASE_DIR))

# Import the approved metrics
from semantic_layer.metrics import get_metric


# Location of the dataset
DATA_FILE = BASE_DIR / "data" / "sales.csv"


# Load the dataset
df = pd.read_csv(DATA_FILE)


def calculate_metric(metric_name, region=None, product=None):
    """
    Calculate an approved business metric using the actual dataset.
    """

    # Get the metric definition from the Semantic Layer
    metric = get_metric(metric_name)

    # Make a copy of the dataset
    filtered_df = df.copy()

    # Apply region filter
    if region:
        filtered_df = filtered_df[
            filtered_df["region"].str.lower() == region.lower()
        ]

    # Apply product filter
    if product:
        filtered_df = filtered_df[
            filtered_df["product"].str.lower() == product.lower()
        ]

    # Calculate the requested metric
    if metric_name == "revenue":
        value = filtered_df["revenue"].sum()

    elif metric_name == "cost":
        value = filtered_df["cost"].sum()

    elif metric_name == "profit":
        value = (
            filtered_df["revenue"].sum()
            - filtered_df["cost"].sum()
        )

    elif metric_name == "margin":
        revenue = filtered_df["revenue"].sum()
        cost = filtered_df["cost"].sum()

        if revenue == 0:
            value = 0
        else:
            value = (revenue - cost) / revenue * 100

    else:
        raise ValueError("Unsupported metric")

    return {
        "metric": metric["name"],
        "formula": metric["formula"],
        "value": round(value, 2),
        "region": region,
        "product": product,
        "rows_analyzed": len(filtered_df)
    }


# Test the Semantic Engine
if __name__ == "__main__":

    result = calculate_metric(
        metric_name="revenue",
        region="Europe"
    )

    print(result)