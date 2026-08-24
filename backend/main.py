from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

from backend.query_parser import parse_question
from backend.semantic_engine import calculate_metric


# Create FastAPI application
app = FastAPI(
    title="MetricMind API",
    description="Governed Conversational Business Intelligence API",
    version="1.0.0"
)


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_FILE = BASE_DIR / "frontend" / "index.html"


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home page
@app.get("/")
def home():
    return FileResponse(FRONTEND_FILE)


# Ask MetricMind
@app.post("/api/ask")
def ask_question(request: dict):

    # Get the user's question
    question = request.get("question", "").strip()

    # Check if question is empty
    if not question:
        return {
            "success": False,
            "message": "Please enter a business question."
        }

    # Convert natural language into structured intent
    intent = parse_question(question)

    # Check whether a metric was detected
    if not intent["metric"]:
        return {
            "success": False,
            "question": question,
            "message": "Could not identify a supported metric.",
            "intent": intent
        }

    # Calculate the metric using the Semantic Engine
    try:

        result = calculate_metric(
            metric_name=intent["metric"],
            region=intent["region"],
            product=intent["product"]
        )

    except Exception as e:

        return {
            "success": False,
            "question": question,
            "message": f"Unable to calculate the metric: {str(e)}",
            "intent": intent
        }

    # Return the governed result
    return {
        "success": True,
        "question": question,
        "intent": intent,
        "result": result
    }