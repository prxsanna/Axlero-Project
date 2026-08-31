# MetricMind — PostgreSQL Database Guide

This guide explains how PostgreSQL is configured, connected, and utilized as the authoritative data foundation for MetricMind.

---

## 1. PostgreSQL Prerequisites & Setup

### Database Details:
- **Default Database**: `metricmind`
- **Host**: `localhost`
- **Port**: `5432`
- **User**: `postgres`
- **Tables**: `sales`, `products`, `customers`, `customer_status`

### Environment Configuration:
Set your credentials in `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=metricmind
DB_USER=postgres
DB_PASSWORD=your_password_here
```

---

## 2. Connection Architecture

MetricMind connects using SQLAlchemy 2.0 connection pooling (`backend/database.py`):

```python
from backend.database import get_engine, check_connection, execute_raw_sql

# Test connection health
status = check_connection()
print(status)
# {'status': 'connected', 'host': 'localhost', 'port': '5432', 'database': 'metricmind'}
```

---

## 3. Querying Through the Semantic Layer

Application components do not execute unconstrained SQL. All analytical queries pass through `GovernedSemanticEngine`:

```python
from backend.app.semantic.layer import GovernedSemanticEngine
from backend.app.semantic.models import SemanticQueryRequest, FilterCondition

# Example: Governed European revenue query
req = SemanticQueryRequest(
    measures=["revenue", "cost", "profit", "margin_pct"],
    dimensions=["quarter"],
    filters=[FilterCondition(dimension="region", operator="=", value="Europe")]
)

res = GovernedSemanticEngine.execute_query(req)
print(res.data)
```
