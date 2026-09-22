# MetricMind — Cube.dev Integration Guide

## 1. Overview

MetricMind uses Cube.dev as the governed semantic layer between the PostgreSQL data warehouse and the application/AI layer.

The implemented architecture is:

PostgreSQL → dbt → Cube.dev → FastAPI → MetricMind Agent/LangChain → Frontend

Cube.dev provides centralized metric definitions, governed query generation, and API-based access for business analytics.

## 2. Project Architecture

The Cube.dev integration follows this flow:

```text
User
  ↓
MetricMind Frontend
  ↓
FastAPI Backend
  ↓
MetricMind Agent / LangChain
  ↓
Governed Semantic Engine
  ↓
Cube.dev REST API
  ↓
Cube.dev Semantic Layer
  ↓
PostgreSQL
  ↓
dbt fct_sales

## 3. PostgreSQL Data Source

MetricMind uses PostgreSQL as the underlying database.

The main analytical table used by Cube.dev is:

```text
fct_sales

## 4. Cube.dev Configuration

Cube.dev is run using Docker.

The Cube configuration files are located in:

```text
cube/docker-compose.yml
cube/cube.js

## 5. Cube.js Configuration

The Cube.js configuration is located at:

```text
cube/cube.js
The current configuration is:

```javascript
module.exports = {
  driverFactory: () => ({
    type: 'postgres',
  }),

  checkAuth: (req, auth) => {},
};

## 6. Environment Variables

The backend uses the following Cube.dev settings from the project root `.env` file:

```env
CUBE_API_URL=http://localhost:4000/cubejs-api/v1/load
CUBE_API_SECRET=<cube-api-secret>

## 7. Cube.dev REST API

Cube.dev exposes the REST API through:

```text
http://localhost:4000/cubejs-api/v1/load
```

The FastAPI backend sends governed Cube queries to this endpoint.

A typical Cube query contains measures and dimensions, for example:

```json
{
  "measures": ["sales.revenue"],
  "dimensions": ["sales.region"]
}
```

The backend authenticates the request using the Cube API secret:

```text
Authorization: Bearer <cube-api-secret>
```

The Cube response is then returned to the MetricMind semantic layer for further processing.

## 8. FastAPI → Cube.dev Integration

The Cube.dev integration is implemented in:

```text
backend/app/semantic/layer.py
```

The governed semantic engine performs the following steps:

1. Validates the requested metrics, dimensions, and filters.
2. Converts the request into a Cube.dev query.
3. Sends the query to the Cube REST API.
4. Receives the Cube.dev result.
5. Returns the governed result to the application.

The Cube API is accessed using:

```python
cube_headers = {
    "Authorization": f"Bearer {CUBE_API_SECRET}"
}
```

The backend uses a 10-second HTTP timeout for Cube.dev requests:

```python
with httpx.Client(timeout=10.0) as client:
```

When Cube.dev successfully returns data, the response identifies the source as:

```text
Cube.dev Semantic Layer (sales_analytics)
```
## 9. Agent / LangChain Integration

The MetricMind Agent is implemented in:

```text
backend/app/agent/agent.py
```

The Agent receives a natural-language business question and resolves it into a governed analytical request.

The main flow is:

```text
Natural-language Question
        ↓
MetricMind Agent
        ↓
Intent Resolution
        ↓
Governed Tool Selection
        ↓
Governed Semantic Engine
        ↓
Cube.dev REST API
        ↓
Cube.dev Semantic Layer
        ↓
PostgreSQL
```

For example, a revenue question can be resolved to the governed `get_revenue` tool.

The Agent receives the result from the semantic layer and generates the final explanation shown to the user.

The reasoning trace can identify the Cube.dev execution path as:

```text
Cube.dev REST API (/cubejs-api/v1/load)
```

and the returned source as:

```text
Cube.dev Semantic Layer (sales_analytics)
```

## 10. PostgreSQL Fallback

The governed semantic engine includes a PostgreSQL fallback path.

### Primary path

```text
Cube.dev available
        ↓
Cube.dev REST API
        ↓
Cube.dev Semantic Layer
```

### Fallback path

```text
Cube.dev unavailable or returns an error
        ↓
Governed PostgreSQL query
        ↓
fct_sales
```

The fallback uses the application's governed metric and dimension definitions rather than allowing arbitrary SQL generation.

The backend reports the actual execution source so that the frontend can distinguish between:

```text
Cube.dev Semantic Layer (sales_analytics)
```

and:

```text
Governed Semantic Layer (PostgreSQL / fct_sales)
```
## 11. Verified Demo Queries

The following queries were tested through the MetricMind application and confirmed to use the Cube.dev semantic layer.

### Query 1

```text
What was the total revenue for Analytics Pro in North America?
```

Result:

```text
$374,612.46
```

Data source:

```text
Cube.dev Semantic Layer (sales_analytics)
```

### Query 2

```text
What was the total revenue for Cloud Pro in Europe?
```

Result:

```text
$374,082.67
```

Data source:

```text
Cube.dev Semantic Layer (sales_analytics)
```

### Query 3

```text
How many units of Security Enterprise were sold in Asia?
```

Result:

```text
1,681 units
```

Data source:

```text
Cube.dev Semantic Layer (sales_analytics)
```

These tests confirmed the frontend, FastAPI backend, MetricMind Agent, governed semantic engine, Cube.dev, and PostgreSQL are working together for the tested queries.

## 12. Running the Complete Application

### Step 1 — Start Docker Desktop

Make sure Docker Desktop is running.

### Step 2 — Start Cube.dev

From the project root:

```powershell
docker compose -f cube\docker-compose.yml up
```

Cube.dev should be available at:

```text
http://localhost:4000
```

### Step 3 — Activate the Python virtual environment

Open another terminal:

```powershell
cd C:\Users\amalr\OneDrive\Desktop\repository\Axlero-Project
.\venv\Scripts\Activate.ps1
```

### Step 4 — Start FastAPI

```powershell
python -m uvicorn backend.main:app --port 8000
```

FastAPI should be available at:

```text
http://127.0.0.1:8000
```

### Step 5 — Open the MetricMind frontend

Open:

```text
http://localhost:8000
```

Keep the Cube.dev and FastAPI terminals running while using the application.

## 13. Git and Security

The following files contain local configuration and secrets:

```text
.env
cube/.env
```

These files must remain ignored by Git.

Before committing changes, verify:

```powershell
git status --short --ignored
```

The environment files should appear as ignored files and must not be staged.

Never place real PostgreSQL passwords or Cube.dev API secrets in:

- Git commits
- Documentation
- Screenshots
- Public repositories

Use placeholders such as:

```text
<database-password>
<cube-api-secret>
```

when documenting configuration.

## 14. Current Integration Status

The Cube.dev integration has been implemented and tested across the main MetricMind application flow.

Completed:

- Cube.dev Docker setup
- PostgreSQL connection
- Cube semantic model
- Governed business metrics
- Cube REST API configuration
- FastAPI → Cube.dev integration
- MetricMind Agent → semantic layer integration
- Frontend Cube.dev transparency
- PostgreSQL fallback path
- `/api/chat` verification
- `/api/ask` verification
- End-to-end demo query verification
- Git commit and push of the integration code

The current tested architecture is:

```text
PostgreSQL
    ↓
dbt / fct_sales
    ↓
Cube.dev
    ↓
FastAPI
    ↓
MetricMind Agent / LangChain
    ↓
Frontend
```

The integration guide documents the configuration and operation of the Cube.dev layer without exposing credentials.S