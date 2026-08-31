# MetricMind — System Architecture

MetricMind is an enterprise Conversational Business Intelligence and Semantic BI system that translates natural-language business questions into governed, reliable insights without allowing the AI to invent metrics or execute arbitrary SQL.

---

## 1. High-Level Data Flow

```
                      User (Natural Language Prompt)
                                    │
                                    ▼
                      [ Next.js 14 Web Workspace ]
                      (ECharts Visualizations + Inspector)
                                    │
                                    ▼ HTTP (POST /api/chat)
                      [ FastAPI Backend Server ]
                                    │
                                    ▼
                      [ LangChain + Google Gemini ]
                      ├── 1. Prompt Safety & SQL Injection Inspection
                      ├── 2. Intent Parsing (Measures, Dimensions, Filters)
                      └── 3. Governed Semantic Tool Selection
                                    │
                                    ▼ Structured Semantic Query
                      [ Governed Semantic Layer / Cube.dev ]
                      ├── Authoritative METRICS_DICTIONARY
                      ├── Authoritative DIMENSIONS_DICTIONARY
                      └── Compiles Parameterized PostgreSQL SQL
                                    │
                                    ▼ Parameterized SQL Execution
                      [ dbt Marts / PostgreSQL Database ]
                      ├── sales (50,000 transactions)
                      ├── customers (10,000 customers)
                      ├── products (20 catalog products)
                      └── customer_status (10,000 status records)
                                    │
                                    ▼ Structured JSON Result
                      [ Multi-Step Synthesis & ECharts Builder ]
                      ├── Executive Markdown Answer
                      ├── Multi-step Reasoning Trace
                      └── Dynamic ECharts Visual Specification
                                    │
                                    ▼ JSON Response
                      [ Next.js / Web Chat Interface ]
```

---

## 2. Component Responsibilities

| Layer | Technology | Primary Responsibility |
|---|---|---|
| **Frontend** | Next.js 14 / React 18 / Tailwind CSS / ECharts | Natural-language query interface, interactive charts, metric catalog sidebar, and query transparency inspector. |
| **Backend API** | FastAPI / Pydantic / Uvicorn | Request validation, CORS management, routing, health checks, and static asset serving. |
| **Orchestration** | LangChain / Google Gemini 3.6 Flash | Natural language understanding, governed tool execution, multi-step causal reasoning, and executive answer synthesis. |
| **Governance** | GovernanceGuardrails | Regex & AST prompt inspection blocking `DROP`, `DELETE`, `TRUNCATE`, `INSERT`, `ALTER`, and unauthorized metric/dimension requests. |
| **Semantic Layer** | Cube.dev / GovernedSemanticEngine | Single source of truth for business metric definitions (`revenue`, `cost`, `profit`, `margin_pct`, `quantity`, `shipping_cost`, `material_cost`). |
| **Transformation** | dbt (data build tool) | Staging views (`stg_sales`, `stg_products`, `stg_customers`) and analytical dimensional marts (`fct_sales`, `dim_products`, `dim_customers`). |
| **Database** | PostgreSQL | Authoritative relational data warehouse storing sales, product, and customer records. |

---

## 3. Anti-Pattern Prevention

MetricMind strictly prohibits the vulnerable direct SQL generation pattern:
```
❌ Anti-Pattern: User -> LLM -> Arbitrary SQL -> PostgreSQL (PROHIBITED)
```

Instead, MetricMind enforces governed semantic tool calling:
```
✅ Governed Pattern: User -> LLM Agent -> Governed Semantic Tool -> Parameterized SQL -> PostgreSQL (ENFORCED)
```
