"""
FastAPI REST API Routes for MetricMind.

Provides conversational BI endpoints, direct semantic queries, metric catalogs,
and dataset transparency.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

from backend.app.semantic.models import SemanticQueryRequest, SemanticQueryResponse, FilterCondition
from backend.app.semantic.layer import GovernedSemanticEngine
from backend.app.semantic.metadata import METRICS_DICTIONARY, DIMENSIONS_DICTIONARY
from backend.app.agent.agent import MetricMindAgent
from backend.app.core.governance import PromptInjectionError
from backend.database import check_connection, execute_raw_sql

router = APIRouter(prefix="/api")
agent_instance = MetricMindAgent()


class ChatRequest(BaseModel):
    prompt: str = Field(..., description="Natural language business question")


class AskRequest(BaseModel):
    question: str = Field(..., description="Business question for MetricMind")


@router.post("/chat")
def chat_endpoint(request: ChatRequest) -> Dict[str, Any]:
    """
    Primary Conversational BI Endpoint for Next.js / Web Frontend.
    Accepts natural language business questions and returns governed analytical answers,
    multi-step reasoning traces, ECharts configs, and query transparency details.
    """
    try:
        response = agent_instance.process_query(request.prompt)
        return response
    except PromptInjectionError as pie:
        raise HTTPException(status_code=400, detail=str(pie))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution error: {str(e)}")


@router.post("/ask")
def ask_endpoint(request: AskRequest) -> Dict[str, Any]:
    """
    Backward-compatible endpoint for MetricMind PoC clients.
    """
    try:
        response = agent_instance.process_query(request.question)
        if response.get("status") == "success":
            return {
                "success": True,
                "question": request.question,
                "answer": response.get("answer"),
                "metric": response.get("metric"),
                "definition": METRICS_DICTIONARY.get(response.get("metric", "revenue"), {}).get("description", ""),
                "formula": METRICS_DICTIONARY.get(response.get("metric", "revenue"), {}).get("sql_formula", ""),
                "filters": response.get("transparency", {}).get("api_calls", [{}])[0].get("request", {}).get("filters", []),
                "rows_used": response.get("transparency", {}).get("total_rows_scanned", 0),
                "explanation": response.get("explanation"),
                "chart_config": response.get("chart_config"),
                "governance": {
                    "semantic_layer": "MetricMind Governed Semantic Layer",
                    "raw_sql_generated": False,
                    "metric_validated": True,
                    "data_source": "PostgreSQL (metricmind)"
                }
            }
        else:
            return {
                "success": False,
                "message": response.get("explanation") or "Could not process request."
            }
    except PromptInjectionError as pie:
        return {
            "success": False,
            "message": str(pie)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Query Error: {str(e)}"
        }


@router.post("/semantic/query", response_model=SemanticQueryResponse)
def semantic_query_endpoint(request: SemanticQueryRequest):
    """
    Direct Semantic Layer API Endpoint.
    Validates measures/dimensions against dictionary and returns governed SQL + results.
    """
    response = GovernedSemanticEngine.execute_query(request)
    return response


@router.get("/semantic/metrics")
@router.get("/metrics")
def get_metrics_catalog():
    """
    Returns authoritative catalog of governed metrics and dimensions.
    """
    return {
        "measures": METRICS_DICTIONARY,
        "dimensions": DIMENSIONS_DICTIONARY,
        "metrics": [
            {
                "id": k,
                "name": v["label"],
                "formula": v["sql_formula"],
                "unit": v["unit"],
                "description": v["description"]
            }
            for k, v in METRICS_DICTIONARY.items()
        ]
    }


@router.get("/dataset")
def dataset_summary():
    """
    Returns summary statistics and metadata of the underlying PostgreSQL business dataset & dbt marts.
    """
    try:
        rows_count, _ = execute_raw_sql("SELECT COUNT(*) as cnt FROM fct_sales")
        regions_rows, _ = execute_raw_sql("SELECT DISTINCT region FROM fct_sales ORDER BY region")
        products_rows, _ = execute_raw_sql("SELECT DISTINCT product FROM fct_sales ORDER BY product")
        categories_rows, _ = execute_raw_sql("SELECT DISTINCT category FROM fct_sales ORDER BY category")

        return {
            "database": "PostgreSQL (metricmind)",
            "dbt_mart": "fct_sales",
            "total_sales_rows": rows_count[0]["cnt"] if rows_count else 0,
            "regions": [r["region"] for r in regions_rows],
            "products": [p["product"] for p in products_rows],
            "categories": [c["category"] for c in categories_rows],
            "metrics": list(METRICS_DICTIONARY.keys()),
            "dimensions": list(DIMENSIONS_DICTIONARY.keys())
        }
    except Exception as e:
        return {
            "database": "PostgreSQL (metricmind)",
            "error": str(e)
        }


@router.get("/query")
def query_metric_direct(
    metric: str,
    region: Optional[str] = None,
    product: Optional[str] = None
):
    """
    Direct parameter query for single metric calculation.
    """
    metric_clean = metric.lower().strip()
    if metric_clean not in METRICS_DICTIONARY:
        raise HTTPException(status_code=400, detail=f"Unknown metric '{metric}'.")

    filters = []
    if region:
        filters.append(FilterCondition(dimension="region", operator="=", value=region))
    if product:
        filters.append(FilterCondition(dimension="product", operator="=", value=product))

    req = SemanticQueryRequest(
        measures=[metric_clean],
        filters=filters
    )
    res = GovernedSemanticEngine.execute_query(req)
    if res.status != "success":
        raise HTTPException(status_code=400, detail=res.error_message)

    return res.model_dump()


@router.get("/health")
def health_check():
    """
    Comprehensive health check verifying PostgreSQL database connection.
    """
    db_status = check_connection()
    return {
        "status": "healthy" if db_status.get("status") == "connected" else "degraded",
        "service": "MetricMind Governed BI Engine",
        "semantic_layer": "active",
        "database": db_status
    }
