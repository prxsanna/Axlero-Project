# MetricMind — API Reference

FastAPI backend endpoints available at `http://localhost:8000`.

---

## 1. Primary Conversational BI Endpoint

### `POST /api/chat`
Accepts natural-language business questions and returns governed analytical results, reasoning trace steps, and ECharts visualization configs.

**Request**:
```json
{
  "prompt": "How much revenue did we make in Europe?"
}
```

**Response**:
```json
{
  "query": "How much revenue did we make in Europe?",
  "status": "success",
  "answer": "$9,809,305.67",
  "metric": "revenue",
  "explanation": "### Governed Analytics: Revenue (Filters: region = 'Europe')\n\n- **Revenue**: **$9,809,305.67** `(Formula: SUM(s.revenue))`",
  "chart_config": null,
  "reasoning_steps": [
    {
      "step": 1,
      "action": "Gemini Intent Parsing & Semantic Resolution",
      "thought": "Parsed measures=['revenue'], dimensions=[], filters=[{'dimension': 'region', 'operator': '=', 'value': 'Europe'}]"
    },
    {
      "step": 2,
      "action": "Execute Governed Semantic Query",
      "generated_sql": "SELECT SUM(s.revenue) AS revenue FROM sales s ...",
      "row_count": 1
    }
  ],
  "transparency": {
    "api_calls": [...],
    "governed_metrics_used": ["revenue"],
    "data_source": "PostgreSQL (metricmind.sales)",
    "total_rows_scanned": 1,
    "execution_time_ms": 12.4
  }
}
```

---

## 2. Compatibility PoC Endpoint

### `POST /api/ask`
**Request**:
```json
{
  "question": "What is our profit?"
}
```

---

## 3. Direct Semantic Layer Query

### `POST /api/semantic/query`
**Request**:
```json
{
  "measures": ["revenue", "profit", "margin_pct"],
  "dimensions": ["region"],
  "filters": [],
  "limit": 10
}
```

---

## 4. Metadata Endpoints

- `GET /api/health`: Database connection status.
- `GET /api/metrics` / `GET /api/semantic/metrics`: Catalog of measures and dimensions.
- `GET /api/dataset`: Summary statistics of sales records, regions, products, and categories.
- `GET /api/query?metric=revenue&region=Europe`: Direct parameter-based query.
