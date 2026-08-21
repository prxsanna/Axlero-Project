"""
MetricMind Query Parser

This is the Day-1 fallback parser.

It converts natural-language questions into
MetricMind's governed metric names.

Later, Gemini will perform this intent extraction.
"""

import re


REGIONS = [
    "Europe",
    "Asia",
    "North America"
]


PRODUCTS = [
    "Software",
    "Hardware",
    "Services"
]


# =========================================================
# METRIC SYNONYMS
# =========================================================

METRIC_SYNONYMS = {

    "revenue": [
        "revenue",
        "sales",
        "income",
        "earnings",
        "money made",
        "money we made",
        "amount made",
        "turnover",
        "generated",
        "made from",
        "made in",
        "how much did we make",
        "how much money did we make",
        "how much money we made"
    ],

    "cost": [
        "cost",
        "costs",
        "expense",
        "expenses",
        "spending",
        "spent"
    ],

    "profit": [
        "profit",
        "profits",
        "profitability",
        "net profit",
        "money earned"
    ],

    "margin": [
        "margin",
        "margins",
        "profit margin",
        "margin percentage",
        "profit percentage"
    ]
}


# =========================================================
# DETECT METRIC
# =========================================================

def detect_metric(question: str):

    q = question.lower().strip()

    # Check longer phrases first.
    # This prevents short words from interfering.

    for metric, phrases in METRIC_SYNONYMS.items():

        for phrase in phrases:

            if phrase in q:

                return metric

    return None


# =========================================================
# DETECT REGION
# =========================================================

def detect_region(question: str):

    q = question.lower()

    for region in REGIONS:

        if region.lower() in q:

            return region

    return None


# =========================================================
# DETECT PRODUCT
# =========================================================

def detect_product(question: str):

    q = question.lower()

    for product in PRODUCTS:

        if product.lower() in q:

            return product

    return None


# =========================================================
# PARSE QUESTION
# =========================================================

def parse_question(question: str):

    metric = detect_metric(question)

    region = detect_region(question)

    product = detect_product(question)

    return {

        "metric": metric,

        "region": region,

        "product": product

    }