# MetricMind --- PostgreSQL Database Guide

## 1. Purpose

PostgreSQL is the current database foundation for MetricMind. It stores
the structured business data used to calculate governed metrics such as
Revenue, Cost, Profit and Margin.

The current PostgreSQL setup is the working foundation for the PoC. It
should not be replaced simply because another database is available.

## 2. Where PostgreSQL fits

``` text
User
  |
  v
MetricMind Frontend
  |
  v
FastAPI Backend
  |
  v
AI / Query Understanding
  |
  v
Semantic Layer
  |
  v
PostgreSQL
  |
  v
Business Data
```

The key separation is:

``` text
AI understands the question
        |
        v
Semantic Layer defines the metric
        |
        v
PostgreSQL provides the actual data
        |
        v
MetricMind calculates the result
```

The LLM should not invent the final business number.

## 3. Why PostgreSQL is used

PostgreSQL gives MetricMind a proper relational database instead of
relying only on CSV files.

It provides:

-   Structured tables and relationships.
-   SQL querying.
-   A stable data source for the backend.
-   A database that Cube.dev can connect to.
-   A database that dbt can model/transform.
-   A practical foundation for the current PoC.

## 4. How PostgreSQL is used in the project

The database foundation includes:

-   Creating the MetricMind PostgreSQL database.
-   Creating the required business tables.
-   Loading sample/dummy business data.
-   Connecting the backend to PostgreSQL.
-   Making the data available to the semantic layer.
-   Maintaining the schema for future Cube.dev/dbt integration.

The project documentation describes the database as having four core
tables and recommends documenting their columns and relationships before
changing fields used by downstream components.

## 5. Backend connection

The backend contains:

``` text
backend/database.py
```

This module is responsible for the application's database connection.

Conceptually:

``` text
FastAPI
   |
   v
backend/database.py
   |
   v
PostgreSQL
```

Database credentials should be stored in environment variables rather
than source code.

Example:

``` env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=metricmind
DB_USER=postgres
DB_PASSWORD=your_password
```

Never commit real passwords, API keys, or `.env` files to GitHub.

## 6. Example: a business question

Suppose the user asks:

> How much money did we make from Europe?

The intended flow is:

``` text
User Question
      |
      v
AI / Query Understanding
      |
      v
Structured Intent

metric = revenue
region = Europe
      |
      v
Semantic Layer
      |
      v
Revenue = SUM(revenue)
      |
      v
PostgreSQL
      |
      v
Filter Europe data
      |
      v
Calculate actual Revenue
      |
      v
Return result
```

The AI understands the question.

The semantic layer defines the calculation.

PostgreSQL supplies the actual data.

## 7. Why the Semantic Layer matters

We do not want:

``` text
User
  |
  v
LLM
  |
  v
LLM invents a calculation
```

Instead:

``` text
User
  |
  v
LLM
  |
  v
metric = revenue
region = Europe
  |
  v
Semantic Layer
  |
  v
Revenue = SUM(revenue)
  |
  v
PostgreSQL
  |
  v
Actual Result
```

The current Python semantic layer is the initial implementation. The
team is now working toward reproducing the governed metric definitions
with Cube.dev/dbt.

## 8. PostgreSQL → Cube.dev

The planned architecture is:

``` text
PostgreSQL
     |
     v
Cube.dev
     |
     v
Governed Metrics
     |
     v
FastAPI / Agent
     |
     v
LangChain + LLM
     |
     v
MetricMind
```

The first Cube.dev milestone is to connect Cube.dev to PostgreSQL and
successfully return one verified metric, such as Revenue.

After that, additional metrics can be added.

## 9. PostgreSQL → dbt

dbt can provide a transformation/modeling layer:

``` text
PostgreSQL Raw Tables
        |
        v
       dbt
        |
        v
Clean / Metric-ready Models
        |
        v
Cube.dev
        |
        v
MetricMind
```

dbt and Cube.dev should use consistent business definitions rather than
competing formulas.

## 10. Why we are not immediately moving to Snowflake/Databricks

Snowflake and Databricks are part of the broader target architecture,
but they are not necessary to prove the current PostgreSQL-based PoC.

The incremental approach is:

``` text
Current:
PostgreSQL → Semantic Layer → FastAPI → AI

Next:
PostgreSQL → dbt/Cube.dev → LangChain/LLM → FastAPI/Frontend

Future, if justified:
Production Data → Snowflake/Databricks → dbt/Cube.dev
                 → Agent/FastAPI → MetricMind
```

Changing the database can affect existing code and integrations.
Therefore, a replacement should only be recommended if it provides clear
value.

## 11. Responsibilities around the database

### Prasanna

-   Own the database foundation.
-   Maintain the architecture and backend/database integration.
-   Coordinate changes that affect Cube.dev, dbt or the AI layer.
-   Lead overall integration and testing.

### Trisha

-   Review and validate the database/data.
-   Evaluate suitable real datasets.
-   Work on dbt/data modeling.
-   Help ensure the database remains metric-ready.

### Sooraj / Amal

-   Connect Cube.dev to PostgreSQL.
-   Create governed Cube models.
-   Reproduce the approved business metrics.
-   Keep metric definitions aligned with the database/model.

### Nanditha

-   Build the LangChain/Llama 3 agent flow.
-   Connect the agent to governed semantic tools rather than
    unrestricted SQL.

## 12. Database change rule

Before changing the schema:

1.  Confirm the change is necessary.
2.  Check backend dependencies.
3.  Check dbt dependencies.
4.  Check Cube.dev dependencies.
5.  Inform affected team members.
6.  Test the application.
7.  Document the change.
8.  Commit the change to the appropriate branch.

Avoid changing table names or columns casually because other components
may depend on them.

## 13. Current status

### Working foundation

``` text
PostgreSQL
    |
    v
Backend database integration
    |
    v
MetricMind PoC
```

### In progress

``` text
PostgreSQL
    |
    +----> dbt / data modeling
    |
    +----> Cube.dev semantic layer
    |
    +----> LangChain / LLM agent
```

### Future

``` text
Governed semantic queries
        |
        v
Multi-step reasoning
        |
        v
Charts / drill-downs
        |
        v
Production warehouse
        |
        v
Governance + evaluation
```

## 14. Key takeaway

PostgreSQL is the **data foundation**, not the AI component.

``` text
PostgreSQL
= stores business data

Semantic Layer
= defines what metrics mean

Cube.dev / dbt
= future governed modeling/semantic infrastructure

LangChain + LLM
= understands and orchestrates questions

FastAPI
= connects components

Frontend
= user interface
```

The objective is to keep these responsibilities separate so the AI can
understand business questions without being trusted to invent business
calculations.
