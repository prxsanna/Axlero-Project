"""
MetricMind Gemini Agent

Gemini's job:
    Understand the user's natural-language question.

Gemini does NOT:
    - calculate revenue
    - calculate margin
    - access the CSV
    - generate SQL

Gemini only converts the question into
a controlled MetricMind intent.
"""

import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# CREATE GEMINI CLIENT
# =========================================================

if API_KEY:

    client = genai.Client(
        api_key=API_KEY
    )

else:

    client = None


# =========================================================
# ALLOWED VALUES
# =========================================================

ALLOWED_METRICS = [
    "revenue",
    "cost",
    "profit",
    "margin"
]


ALLOWED_REGIONS = [
    "Europe",
    "Asia",
    "North America"
]


ALLOWED_PRODUCTS = [
    "Software",
    "Hardware",
    "Services"
]


# =========================================================
# GEMINI INTENT EXTRACTION
# =========================================================

def extract_intent(question: str):

    """
    Convert natural language into a controlled
    MetricMind query.

    Example:

    User:
        How much money did we make from Europe?

    Gemini:

        {
            "metric": "revenue",
            "region": "Europe",
            "product": null
        }
    """

    if not client:

        return None


    prompt = f"""
You are the natural-language intent engine
for a Business Intelligence system called MetricMind.

Your ONLY job is to identify which approved business
metric and filters the user is asking for.

You must NOT calculate the answer.

You must NOT generate SQL.

You must NOT invent metrics.

You must only select from the approved values below.

APPROVED METRICS:

- revenue
- cost
- profit
- margin

APPROVED REGIONS:

- Europe
- Asia
- North America

APPROVED PRODUCTS:

- Software
- Hardware
- Services

METRIC MEANINGS:

revenue:
Total money generated from sales.

cost:
Total cost associated with sales.

profit:
Revenue minus Cost.

margin:
(Revenue - Cost) / Revenue.

IMPORTANT INTERPRETATION RULES:

"sales", "money made", "money earned",
"amount generated", "income", "turnover"
usually mean revenue.

"spent", "expenses", "spending", "costs"
usually mean cost.

"profitability", "profit earned"
usually mean profit.

"margin percentage", "profit margin"
means margin.

The user question is:

{question}

Return ONLY valid JSON.

The JSON must have exactly these fields:

{{
    "metric": "revenue",
    "region": "Europe",
    "product": null
}}

If a region is not mentioned, use null.

If a product is not mentioned, use null.

If the question cannot be mapped to an approved metric,
use null for metric.
"""


    try:

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt,

            config=types.GenerateContentConfig(

                response_mime_type="application/json",

                response_schema={
                    "type": "object",

                    "properties": {

                        "metric": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "enum": [
                                "revenue",
                                "cost",
                                "profit",
                                "margin",
                                None
                            ]
                        },

                        "region": {
                            "type": [
                                "string",
                                "null"
                            ]
                        },

                        "product": {
                            "type": [
                                "string",
                                "null"
                            ]
                        }

                    },

                    "required": [
                        "metric",
                        "region",
                        "product"
                    ]
                }

            )

        )


        result = json.loads(
            response.text
        )


        return validate_intent(result)


    except Exception as error:

        print(
            "Gemini error:",
            error
        )

        return None


# =========================================================
# VALIDATE GEMINI OUTPUT
# =========================================================

def validate_intent(intent):

    """
    Never trust the LLM output blindly.

    Validate everything against our approved
    Semantic Layer values.
    """

    if not isinstance(intent, dict):

        return None


    metric = intent.get(
        "metric"
    )

    region = intent.get(
        "region"
    )

    product = intent.get(
        "product"
    )


    # -----------------------------------------------------
    # Validate metric
    # -----------------------------------------------------

    if metric is not None:

        if metric not in ALLOWED_METRICS:

            return None


    # -----------------------------------------------------
    # Validate region
    # -----------------------------------------------------

    if region is not None:

        if region not in ALLOWED_REGIONS:

            region = None


    # -----------------------------------------------------
    # Validate product
    # -----------------------------------------------------

    if product is not None:

        if product not in ALLOWED_PRODUCTS:

            product = None


    return {

        "metric": metric,

        "region": region,

        "product": product

    }