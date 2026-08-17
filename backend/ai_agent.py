"""
MetricMind Gemini Agent

The LLM is used to understand the user's question.

The LLM does NOT directly access the database.

Instead, it returns a structured request
that MetricMind validates before calling
the Semantic Layer.
"""

import os
import json

from google import genai
from google.genai import types


# =========================================================
# CLIENT
# =========================================================

API_KEY = os.getenv("GEMINI_API_KEY")


if API_KEY:

    client = genai.Client(
        api_key=API_KEY
    )

else:

    client = None


# =========================================================
# SEMANTIC SCHEMA
# =========================================================

SEMANTIC_SCHEMA = """

MetricMind supports these metrics:

1. revenue
   Formula: SUM(revenue)

2. cost
   Formula: SUM(cost)

3. profit
   Formula: Revenue - Cost

4. margin
   Formula: (Revenue - Cost) / Revenue


Supported regions:

- Europe
- Asia
- North America


Supported products:

- Software
- Hardware
- Services

The model must NEVER invent a new metric.

The model must NEVER generate SQL.

The model must return only the metric and filters
required to query the MetricMind Semantic Layer.

"""


# =========================================================
# INTENT EXTRACTION
# =========================================================

def extract_intent(question: str):

    if not client:

        return None


    prompt = f"""

You are the intent extraction component
of MetricMind.

MetricMind is a governed business intelligence
system.

Your job is to understand the user's question
and map it to the approved Semantic Layer.

{SEMANTIC_SCHEMA}

User question:

{question}

Return JSON only.

Required format:

{{
    "metric": "revenue",
    "region": null,
    "product": null
}}

Rules:

- metric must be one of:
  revenue, cost, profit, margin

- region must be:
  Europe, Asia, North America, or null

- product must be:
  Software, Hardware, Services, or null

- Never invent values.

- Never generate SQL.
"""


    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json"

        )

    )


    return json.loads(response.text)