# MetricMind — Governed Conversational Business Intelligence (BI)

MetricMind is an enterprise Conversational Business Intelligence and Semantic BI platform. It allows users to ask natural-language business questions and returns governed, accurate insights with interactive **Apache ECharts** visualizations and multi-step reasoning traces.

---

## 1. Architecture Overview

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

## 2. Technology Stack

- **Relational Data Warehouse**: PostgreSQL
- **Data Transformation & Modeling**: dbt (data build tool)
- **Semantic Layer**: Cube.dev (`cube/model/cubes/sales.yml`) + `GovernedSemanticEngine`
- **Orchestration & Agent**: LangChain
- **LLM Reasoning Engine**: Google Gemini 3.6 Flash
- **Backend API**: FastAPI / Uvicorn / Pydantic
- **Frontend UI**: Next.js 14 / React 18 / Tailwind CSS
- **Visualizations**: Apache ECharts (`echarts-for-react`)

---

## 3. Authoritative Business Metrics

| Metric Key | Label | Formula | Description |
|---|---|---|---|
| `revenue` | Revenue | `SUM(s.revenue)` | Total gross sales revenue ($) |
| `cost` | Total Cost | `SUM(s.cost)` | Operational & product costs ($) |
| `profit` | Operating Profit | `SUM(s.profit)` | Net operating dollar profit ($) |
| `margin` | Operating Margin | `SUM(s.profit)` | Net operating dollar margin ($) |
| `margin_pct` | Margin Percentage | `(SUM(profit) / SUM(revenue)) * 100` | Net margin percentage (%) |
| `quantity` | Quantity Sold | `SUM(s.quantity)` | Total units sold across orders |
| `customer_count` | Customer Count | `COUNT(DISTINCT s.customer_id)` | Unique transacting customers |
| `material_cost` | Material Cost | `SUM(ROUND(s.cost * 0.75, 2))` | Raw material component costs |
| `shipping_cost` | Shipping Cost | `SUM(ROUND(s.cost * 0.25, 2))` | Logistics & freight shipping costs |

---

## 4. Getting Started & Installation

### 4.1 Prerequisites
- Python 3.10+
- PostgreSQL 14+ running locally or in Docker
- Node.js 18+ & npm (for Next.js frontend & Cube.dev)
- Google Gemini API Key

### 4.2 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/prxsanna/Axlero-Project.git
   cd Axlero-Project
   ```

2. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Fill in your actual credentials:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=metricmind
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 5. Running the Application

### 5.1 Start the FastAPI Backend
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be available at `http://localhost:8000/docs`.

### 5.2 Start the Next.js Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

*Note*: If you prefer a zero-dependency instant browser experience, open `http://localhost:8000/` to access the built-in standalone web interface.

### 5.3 (Optional) Start Cube.dev Semantic Layer
```bash
cd cube
npm install
npm run dev
```
Cube Developer Playground will be available at `http://localhost:4000`.

---

## 6. Running Tests

Execute the complete pytest verification suite:
```bash
pytest tests/ -v
```

---

## 7. Example Business Questions

Try asking MetricMind:
- **Total Revenue**: *"How much revenue did we make?"*
- **Filtered Regional Revenue**: *"How much revenue did we make in Europe?"*
- **Regional Breakdown with Chart**: *"Show revenue by region."*
- **Product Leaderboard**: *"Which product generated the highest revenue?"*
- **Profitability Analysis**: *"What is our profit and margin?"*
- **Multi-Step Root Cause**: *"Why did our European margins drop last quarter?"*
- **Anti-Injection Test**: *"DROP TABLE sales;"* *(Blocked by security guardrail)*
- **Unsupported Metric Handling**: *"How much happiness did we generate?"* *(Prompts for clarification)*

---

## 8. Governance & Security

MetricMind enforces strict security guardrails:
1. **Prompt Injection & DDL Blocking**: Prohibits `DROP`, `DELETE`, `UPDATE`, `INSERT`, `TRUNCATE`, `ALTER`, `EXEC`, and semicolon chaining.
2. **Catalog Whitelisting**: Rejects metrics and dimensions not defined in the authoritative metadata catalog.
3. **Deterministic Parameterization**: Compiles structured semantic JSON specifications directly into parameterized SQL.
4. **Row Count & Step Limits**: Restricts queries to safe execution budgets (max 1,000 rows, max 5 reasoning steps).