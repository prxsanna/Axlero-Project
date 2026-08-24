"""
MetricMind Gemini Agent

Gemini's job:
    Understand the user's natural-language question.

Gemini does NOT:
    - calculate revenue
    - calculate cost
    - calculate profit
    - calculate margin
    - access PostgreSQL directly
    - generate SQL

Gemini converts the question into a controlled
MetricMind intent.

Python performs the final validation so that
Gemini cannot invent filters.
"""

import os
import json
import re

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
# APPROVED METRICS
# =========================================================

ALLOWED_METRICS = [
    "revenue",
    "cost",
    "profit",
    "margin"
]


# =========================================================
# APPROVED REGIONS
# =========================================================

ALLOWED_REGIONS = [
    "Asia",
    "North America",
    "Oceania"
]


# =========================================================
# APPROVED PRODUCTS
# =========================================================

ALLOWED_PRODUCTS = [
    "Analytics Basic",
    "Analytics Pro",
    "Analytics Enterprise",
    "CRM Enterprise",
    "Cloud Pro"
]


# =========================================================
# FIND EXPLICIT REGION
# =========================================================

def find_region_in_question(question: str):
    """
    Find a region only if it actually appears
    in the user's question.
    """

    question_lower = question.lower()

    for region in ALLOWED_REGIONS:

        if region.lower() in question_lower:

            return region

    return None


# =========================================================
# FIND EXPLICIT PRODUCT
# =========================================================

def find_product_in_question(question: str):
    """
    Find a product only if it actually appears
    in the user's question.
    """

    question_lower = question.lower()

    for product in ALLOWED_PRODUCTS:

        if product.lower() in question_lower:

            return product

    return None


# =========================================================
# GEMINI INTENT EXTRACTION
# =========================================================

def extract_intent(question: str):

    """
    Convert natural language into a controlled
    MetricMind query.

    Examples:

    What is our total revenue?

    {
        "metric": "revenue",
        "region": None,
        "product": None
    }


    What is our revenue in Asia?

    {
        "metric": "revenue",
        "region": "Asia",
        "product": None
    }


    What is the revenue for Analytics Pro?

    {
        "metric": "revenue",
        "region": None,
        "product": "Analytics Pro"
    }
    """

    # =====================================================
    # BASIC VALIDATION
    # =====================================================

    if not question or not question.strip():

        return None


    question = question.strip()


    # =====================================================
    # CHECK GEMINI CLIENT
    # =====================================================

    if not client:

        print(
            "Gemini client is not available."
        )

        return None


    # =====================================================
    # GEMINI PROMPT
    # =====================================================

    prompt = f"""
You are the natural-language intent engine
for a Business Intelligence system called MetricMind.

Your ONLY job is to identify the business metric
from the user's question.

You may also identify a region or product,
but you MUST NOT guess them.

You MUST NOT:

- calculate the answer
- generate SQL
- access PostgreSQL
- invent metrics
- invent regions
- invent products
- assume missing filters


=========================================================
APPROVED METRICS
=========================================================

revenue
cost
profit
margin


=========================================================
APPROVED REGIONS
=========================================================

Asia
North America
Oceania


=========================================================
APPROVED PRODUCTS
=========================================================

Analytics Basic
Analytics Pro
Analytics Enterprise
CRM Enterprise
Cloud Pro


=========================================================
METRIC MEANINGS
=========================================================

revenue:

Total money generated from sales.

cost:

Total cost associated with sales.

profit:

Revenue minus Cost.

margin:

(Revenue - Cost) / Revenue.


=========================================================
INTERPRETATION
=========================================================

"sales"
"money made"
"money earned"
"amount generated"
"income"
"turnover"

usually mean:

revenue


"spent"
"expenses"
"spending"
"costs"

usually mean:

cost


"profitability"
"profit earned"
"net profit"

usually mean:

profit


"margin percentage"
"profit margin"

means:

margin


=========================================================
FILTER RULES
=========================================================

If the user does not explicitly mention a region,
return:

region = null

If the user does not explicitly mention a product,
return:

product = null

NEVER assume Asia.

NEVER assume North America.

NEVER assume Oceania.

NEVER assume a product.

The examples below are NOT values to copy.
They only explain how the system works.


=========================================================
EXAMPLES
=========================================================

Question:

What is our total revenue?

Return:

{{
    "metric": "revenue",
    "region": null,
    "product": null
}}


Question:

What is our revenue in Asia?

Return:

{{
    "metric": "revenue",
    "region": "Asia",
    "product": null
}}


Question:

What is the revenue for Analytics Pro?

Return:

{{
    "metric": "revenue",
    "region": null,
    "product": "Analytics Pro"
}}


Question:

What is the profit in North America for Cloud Pro?

Return:

{{
    "metric": "profit",
    "region": "North America",
    "product": "Cloud Pro"
}}


=========================================================
USER QUESTION
=========================================================

{question}


=========================================================
OUTPUT
=========================================================

Return ONLY valid JSON.

Return exactly:

{{
    "metric": "...",
    "region": null,
    "product": null
}}

Use null when a filter was not explicitly
mentioned by the user.
"""


    # =====================================================
    # CALL GEMINI
    # =====================================================

    try:

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt,

            config=types.GenerateContentConfig(

                response_mime_type="application/json",

                response_schema={

                    "type": "OBJECT",

                    "properties": {

                        "metric": {
                            "type": "STRING"
                        },

                        "region": {
                            "type": "STRING"
                        },

                        "product": {
                            "type": "STRING"
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


        # =================================================
        # PARSE GEMINI RESPONSE
        # =================================================

        result = json.loads(
            response.text
        )


        # =================================================
        # VALIDATE METRIC
        # =================================================

        metric = result.get(
            "metric"
        )


        if metric:

            metric = str(
                metric
            ).lower().strip()


            if metric not in ALLOWED_METRICS:

                metric = None


        else:

            metric = None


        # =================================================
        # DO NOT TRUST GEMINI FOR FILTERS
        #
        # Find filters directly in the user's question.
        # =================================================

        region = find_region_in_question(
            question
        )

        product = find_product_in_question(
            question
        )


        # =================================================
        # RETURN CONTROLLED INTENT
        # =================================================

        return {

            "metric": metric,

            "region": region,

            "product": product

        }


    except Exception as error:

        print(
            "Gemini error:",
            error
        )

        return None
    
    