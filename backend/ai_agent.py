import os
import json

from dotenv import load_dotenv
import google.generativeai as genai


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )


# ============================================================
# Configure Gemini
# ============================================================

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")


# ============================================================
# Supported MetricMind definitions
# ============================================================

SUPPORTED_METRICS = [
    "revenue",
    "cost",
    "profit",
    "margin"
]

SUPPORTED_REGIONS = [
    "Europe",
    "Asia",
    "North America"
]

SUPPORTED_PRODUCTS = [
    "Software",
    "Hardware",
    "Services"
]


# ============================================================
# Extract Intent using Gemini
# ============================================================

def extract_intent(question):
    """
    Use Gemini only to understand the user's question.

    Gemini returns:
        metric
        region
        product

    Gemini does NOT calculate the final business value.
    """

    prompt = f"""
You are the intent extraction component of MetricMind.

MetricMind is a governed conversational business intelligence
system.

Your ONLY task is to understand the user's business question
and convert it into structured intent.

Supported metrics:
- revenue
- cost
- profit
- margin

Supported regions:
- Europe
- Asia
- North America

Supported products:
- Software
- Hardware
- Services

Rules:

1. Do NOT calculate any number.
2. Do NOT invent a metric.
3. Do NOT invent a region.
4. Do NOT invent a product.
5. If a region is not mentioned, return null.
6. If a product is not mentioned, return null.
7. Return ONLY valid JSON.
8. Do not include markdown.
9. Do not include explanations.

Example:

User:
What is the revenue in Europe?

Return:

{{
    "metric": "revenue",
    "region": "Europe",
    "product": null
}}

Another example:

User:
What is the software revenue in Asia?

Return:

{{
    "metric": "revenue",
    "region": "Asia",
    "product": "Software"
}}

User question:
{question}
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        # Convert Gemini response into Python dictionary
        intent = json.loads(text)

        return intent

    except json.JSONDecodeError:
        return {
            "metric": None,
            "region": None,
            "product": None,
            "error": "Gemini returned an invalid JSON response."
        }

    except Exception as e:
        return {
            "metric": None,
            "region": None,
            "product": None,
            "error": str(e)
        }


# ============================================================
# Validate Gemini Intent
# ============================================================

def validate_intent(intent):
    """
    Validate the structured intent against
    MetricMind's approved definitions.
    """

    metric = intent.get("metric")
    region = intent.get("region")
    product = intent.get("product")

    # Validate metric
    if metric not in SUPPORTED_METRICS:
        return False, "Unsupported metric."

    # Validate region
    if region is not None and region not in SUPPORTED_REGIONS:
        return False, "Unsupported region."

    # Validate product
    if product is not None and product not in SUPPORTED_PRODUCTS:
        return False, "Unsupported product."

    return True, "Intent is valid."


# ============================================================
# Complete AI Intent Pipeline
# ============================================================

def process_question(question):
    """
    Complete Gemini intent pipeline:

    Question
        ↓
    Gemini
        ↓
    Structured Intent
        ↓
    Validation
    """

    intent = extract_intent(question)

    # Check Gemini error
    if intent.get("error"):
        return {
            "success": False,
            "intent": intent,
            "message": intent["error"]
        }

    # Validate intent
    valid, message = validate_intent(intent)

    if not valid:
        return {
            "success": False,
            "intent": intent,
            "message": message
        }

    return {
        "success": True,
        "intent": intent,
        "message": "Intent validated successfully."
    }


# ============================================================
# Test Gemini Intent Extraction
# ============================================================

if __name__ == "__main__":

    question = "How much money did we make from Europe?"

    result = process_question(question)

    print("\nMetricMind Gemini Result")
    print("------------------------")
    print(result)