"""
MetricMind API

Main FastAPI application for MetricMind Conversational Business Intelligence.
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

from backend.app.api.routes import router as api_router

app = FastAPI(
    title="MetricMind",
    description="Governed Conversational Business Intelligence with PostgreSQL, dbt, Cube.dev, LangChain & Gemini",
    version="1.0.0"
)

# Enable CORS for Next.js and frontend dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router)

# Mount static frontend directory if present
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(frontend_dir):
    app.mount(
        "/",
        StaticFiles(
            directory=frontend_dir,
            html=True
        ),
        name="frontend"
    )

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)