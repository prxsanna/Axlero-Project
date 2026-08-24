"""
MetricMind API

Main FastAPI application.

Flow:

User Question
      ↓
Gemini
      ↓
Controlled Intent
      ↓
MetricMind Semantic Engine
      ↓
PostgreSQL
      ↓
Calculated Metric
      ↓
API Response
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.semantic_engine import (
    calculate_metric,
    get_dataset_summary
)

from backend.ai_agent import extract_intent


# =========================================================
# CREATE APPLICATION
# =========================================================

app = FastAPI(
    title="MetricMind",
    description="Governed Conversational Business Intelligence",
    version="0.1.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# REQUEST MODEL
# =========================================================

class QuestionRequest(BaseModel):

    question: str


# =========================================================
# ROOT API
# =========================================================

@app.get("/api")
def api_root():

    return {
        "name": "MetricMind",
        "version": "0.1.0",
        "status": "running"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/api/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================================
# DATASET INFORMATION
# =========================================================

@app.get("/api/dataset")
def dataset():

    return get_dataset_summary()


# =========================================================
# AVAILABLE METRICS
# =========================================================

@app.get("/api/metrics")
def metrics():

    return {
        "metrics": [

            {
                "name": "Revenue",
                "id": "revenue",
                "formula": "SUM(revenue)"
            },

            {
                "name": "Cost",
                "id": "cost",
                "formula": "SUM(cost)"
            },

            {
                "name": "Profit",
                "id": "profit",
                "formula": "Revenue - Cost"
            },

            {
                "name": "Margin",
                "id": "margin",
                "formula": "(Revenue - Cost) / Revenue"
            }

        ]
    }


# =========================================================
# DIRECT METRIC QUERY
# =========================================================

@app.get("/api/query")
def query_metric(
    metric: str,
    region: str | None = None,
    product: str | None = None
):

    try:

        result = calculate_metric(
            metric=metric,
            region=region,
            product=product
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# =========================================================
# NATURAL LANGUAGE QUESTION
# =========================================================

@app.post("/api/ask")
def ask_metricmind(request: QuestionRequest):

    # -----------------------------------------------------
    # Get the user's question
    # -----------------------------------------------------

    question = request.question.strip()


    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    # =====================================================
    # STEP 1
    # GEMINI UNDERSTANDS THE QUESTION
    # =====================================================

    parsed = extract_intent(
        question
    )


    # -----------------------------------------------------
    # Gemini failed
    # -----------------------------------------------------

    if not parsed:

        return {

            "success": False,

            "message": (
                "Gemini could not understand "
                "the question."
            )

        }


    # -----------------------------------------------------
    # Get controlled values
    # -----------------------------------------------------

    metric = parsed["metric"]

    region = parsed["region"]

    product = parsed["product"]


    # =====================================================
    # STEP 2
    # CHECK METRIC
    # =====================================================

    if not metric:

        return {

            "success": False,

            "message": (
                "I could not identify a supported metric. "
                "Try asking about revenue, cost, profit, "
                "or margin."
            ),

            "available_metrics": [

                "revenue",
                "cost",
                "profit",
                "margin"

            ]

        }


    # =====================================================
    # STEP 3
    # SEMANTIC ENGINE
    # =====================================================

    try:

        result = calculate_metric(

            metric=metric,

            region=region,

            product=product

        )


    except ValueError as error:

        return {

            "success": False,

            "message": str(error)

        }


    # =====================================================
    # STEP 4
    # FORMAT VALUE
    # =====================================================

    value = result["value"]


    if metric == "margin":

        formatted_value = (
            f"{value * 100:.2f}%"
        )

    else:

        formatted_value = (
            f"${value:,.0f}"
        )


    # =====================================================
    # STEP 5
    # BUILD FILTER DESCRIPTION
    # =====================================================

    filter_text = []


    if region:

        filter_text.append(
            f"Region: {region}"
        )


    if product:

        filter_text.append(
            f"Product: {product}"
        )


    if not filter_text:

        filter_text.append(
            "All available data"
        )


    # =====================================================
    # STEP 6
    # FINAL RESPONSE
    # =====================================================

    return {

        "success": True,

        "question": question,

        "answer": formatted_value,

        "metric": result["metric"],

        "definition": result["definition"],

        "formula": result["formula"],

        "filters": result["filters"],

        "rows_used": result["rows_used"],

        "explanation": (

            f"{result['metric']} is "
            f"{formatted_value}. "

            f"The calculation used the "
            f"governed definition "

            f"'{result['formula']}'."

        ),

        "governance": {

            "semantic_layer":
                "MetricMind Semantic Layer",

            "raw_sql_generated":
                False,

            "metric_validated":
                True

        }

    }


# =========================================================
# SERVE FRONTEND
# =========================================================

app.mount(

    "/",

    StaticFiles(
        directory="frontend",
        html=True
    ),

    name="frontend"

)