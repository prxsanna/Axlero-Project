"""
MetricMind Query Parser

Day-1 version:
A deterministic parser is used first.

This gives us a reliable fallback even without an LLM.

Later:
Gemini / LangChain will replace or enhance this module.
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


def detect_metric(question: str):

    q = question.lower()

    # Order matters.
    if "margin" in q:
        return "margin"

    if "profit" in q:
        return "profit"

    if "cost" in q or "expense" in q:
        return "cost"

    if "revenue" in q or "sales" in q:
        return "revenue"

    return None


def detect_region(question: str):

    q = question.lower()

    for region in REGIONS:

        if region.lower() in q:
            return region

    return None


def detect_product(question: str):

    q = question.lower()

    for product in PRODUCTS:

        if product.lower() in q:
            return product

    return None


def parse_question(question: str):

    metric = detect_metric(question)

    region = detect_region(question)

    product = detect_product(question)

    return {
        "metric": metric,
        "region": region,
        "product": product
    }