"""
LangChain + Google Gemini Agent for MetricMind.

Translates natural-language business questions into governed semantic tool calls,
multi-step reasoning plans, evidence-based executive explanations, and dynamic ECharts configs.
"""

import os
import json
import time
import re
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_core.prompts import PromptTemplate

from backend.app.core.governance import GovernanceGuardrails, PromptInjectionError
from backend.app.semantic.metadata import METRICS_DICTIONARY, DIMENSIONS_DICTIONARY
from backend.app.semantic.models import SemanticQueryRequest, FilterCondition
from backend.app.semantic.layer import GovernedSemanticEngine
from backend.app.visualization.builder import EChartsBuilder
from backend.app.agent.tools import (
    ALL_GOVERNED_TOOLS,
    execute_governed_query,
    get_revenue,
    get_cost,
    get_profit,
    get_margin,
    get_sales_by_region,
    get_sales_by_product,
    get_customer_metrics
)

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"


class MetricMindAgent:

    def __init__(self):
        self.client = genai.Client(api_key=API_KEY) if API_KEY else None
        self.tools = ALL_GOVERNED_TOOLS
        self.max_steps = 5
        self.prompt_template = PromptTemplate(
            input_variables=["measures_list", "dimensions_list", "question"],
            template=(
                "You are the intent resolution engine for MetricMind, a Governed Conversational BI platform.\n"
                "Extract the intended measures, grouping dimensions, and filter conditions from the user's business question.\n\n"
                "Governed Measures: {measures_list}\n"
                "Governed Dimensions: {dimensions_list}\n\n"
                "Rules:\n"
                "1. Never invent metric names not in Governed Measures.\n"
                "2. If user asks 'revenue by region', measures=['revenue'], dimensions=['region'].\n"
                "3. If user asks 'which product generated highest revenue', measures=['revenue'], dimensions=['product'], order_by='revenue', limit=10.\n"
                "4. If user asks 'what is our profit', measures=['profit'].\n"
                "5. If user asks 'what is our margin', measures=['margin_pct', 'profit'].\n"
                "6. Return JSON matching the intent schema.\n\n"
                "Question: {question}"
            )
        )

    def process_query(self, user_prompt: str) -> Dict[str, Any]:
        """
        Primary entry point for user business queries.
        Inspects prompt safety, resolves intent via LangChain/Gemini, invokes governed semantic tools,
        synthesizes explanations, and builds ECharts visual configs.
        """
        start_time = time.time()
        user_prompt = user_prompt.strip()

        # Step 0: Prompt Safety & Anti-Injection Guardrail
        GovernanceGuardrails.inspect_prompt_safety(user_prompt)

        reasoning_steps = []

        # Step 1: Multi-Step Root Cause Scenario Detection
        prompt_lower = user_prompt.lower()
        if ("why" in prompt_lower or "cause" in prompt_lower or "drop" in prompt_lower or "decline" in prompt_lower) and ("margin" in prompt_lower or "profit" in prompt_lower or "cost" in prompt_lower):
            return self._execute_root_cause_analysis(user_prompt, reasoning_steps, start_time)

        # Step 2: Intent Resolution via LangChain + Gemini
        intent = self._resolve_intent_with_gemini(user_prompt, reasoning_steps)

        # Step 3: Handle Unsupported / Ambiguous Questions Safely
        if not intent.get("measures") and not intent.get("action") == "catalog":
            return self._build_clarification_response(user_prompt, reasoning_steps, start_time)

        # Step 4: Execute Governed Semantic Query via Tools
        return self._execute_resolved_intent(user_prompt, intent, reasoning_steps, start_time)

    def _resolve_intent_with_gemini(self, prompt: str, reasoning_steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Uses LangChain prompt templates and Gemini to translate natural language into a structured semantic plan.
        """
        measures_list = list(METRICS_DICTIONARY.keys())
        dimensions_list = list(DIMENSIONS_DICTIONARY.keys())
        prompt_lower = prompt.lower()
        
        # Fast extraction for canonical filters
        detected_region = None
        for r in ["Asia", "Europe", "North America", "Oceania", "South America"]:
            if r.lower() in prompt_lower:
                detected_region = r
                break

        detected_product = None
        products_list = [
            "AI Assistant Basic", "AI Assistant Enterprise", "AI Assistant Pro",
            "Analytics Basic", "Analytics Enterprise", "Analytics Pro",
            "Cloud Enterprise", "Cloud Pro", "Cloud Starter",
            "CRM Enterprise", "CRM Pro", "CRM Starter",
            "Data Platform Basic", "Data Platform Enterprise", "Data Platform Pro",
            "Security Basic", "Security Enterprise", "Security Pro",
            "Support Premium", "Support Standard"
        ]
        for p in products_list:
            if p.lower() in prompt_lower:
                detected_product = p
                break

        detected_category = None
        for c in ["Analytics", "Cloud", "Security", "CRM", "Data Platform", "AI", "Support"]:
            if c.lower() in prompt_lower:
                detected_category = c
                break

        # If Gemini client is available, use LangChain prompt template + LLM structured JSON intent extraction
        if self.client:
            sys_instruction = self.prompt_template.format(
                measures_list=measures_list,
                dimensions_list=dimensions_list,
                question=prompt
            )

            try:
                response = self.client.models.generate_content(
                    model=MODEL_NAME,
                    contents=f"Question: {prompt}",
                    config=types.GenerateContentConfig(
                        system_instruction=sys_instruction,
                        response_mime_type="application/json",
                        response_schema={
                            "type": "OBJECT",
                            "properties": {
                                "measures": {"type": "ARRAY", "items": {"type": "STRING"}},
                                "dimensions": {"type": "ARRAY", "items": {"type": "STRING"}},
                                "filters": {
                                    "type": "ARRAY",
                                    "items": {
                                        "type": "OBJECT",
                                        "properties": {
                                            "dimension": {"type": "STRING"},
                                            "operator": {"type": "STRING"},
                                            "value": {"type": "STRING"}
                                        },
                                        "required": ["dimension", "operator", "value"]
                                    }
                                },
                                "limit": {"type": "INTEGER"},
                                "order_by": {"type": "STRING"}
                            },
                            "required": ["measures", "dimensions", "filters"]
                        }
                    )
                )
                parsed = json.loads(response.text)
                
                valid_measures = [m for m in parsed.get("measures", []) if m in METRICS_DICTIONARY]
                valid_dimensions = [d for d in parsed.get("dimensions", []) if d in DIMENSIONS_DICTIONARY]
                valid_filters = [f for f in parsed.get("filters", []) if f.get("dimension") in DIMENSIONS_DICTIONARY]

                if detected_region and not any(f.get("dimension") == "region" for f in valid_filters) and "region" not in valid_dimensions:
                    valid_filters.append({"dimension": "region", "operator": "=", "value": detected_region})
                if detected_product and not any(f.get("dimension") == "product" for f in valid_filters) and "product" not in valid_dimensions:
                    valid_filters.append({"dimension": "product", "operator": "=", "value": detected_product})

                reasoning_steps.append({
                    "step": 1,
                    "action": "LangChain + Gemini Intent Parsing & Tool Resolution",
                    "thought": f"Parsed measures={valid_measures}, dimensions={valid_dimensions}, filters={valid_filters}",
                    "query_measures": valid_measures,
                    "query_dimensions": valid_dimensions
                })

                return {
                    "measures": valid_measures,
                    "dimensions": valid_dimensions,
                    "filters": valid_filters,
                    "limit": parsed.get("limit", 100),
                    "order_by": parsed.get("order_by")
                }
            except Exception:
                pass

        # Deterministic Fallback Parser
        measures = []
        dimensions = []
        filters = []

        if "margin percentage" in prompt_lower or "margin %" in prompt_lower or "margin pct" in prompt_lower:
            measures.append("margin_pct")
        elif "margin" in prompt_lower:
            measures.extend(["margin", "margin_pct"])
        elif "profit" in prompt_lower or "earnings" in prompt_lower:
            measures.append("profit")
        elif "cost" in prompt_lower or "expense" in prompt_lower or "spent" in prompt_lower:
            measures.append("cost")
        elif "quantity" in prompt_lower or "units" in prompt_lower or "volume" in prompt_lower:
            measures.append("quantity")
        elif "revenue" in prompt_lower or "sales" in prompt_lower or "turnover" in prompt_lower or "money" in prompt_lower or "make" in prompt_lower:
            measures.append("revenue")

        if "by region" in prompt_lower or "across regions" in prompt_lower:
            dimensions.append("region")
        elif "by product" in prompt_lower or "which product" in prompt_lower or "top product" in prompt_lower or ("highest revenue" in prompt_lower and "product" in prompt_lower):
            dimensions.append("product")
        elif "by category" in prompt_lower or ("category" in prompt_lower and "by" in prompt_lower):
            dimensions.append("category")
        elif "by quarter" in prompt_lower or "over time" in prompt_lower or "by month" in prompt_lower:
            dimensions.append("quarter" if "quarter" in prompt_lower else "month")

        if detected_region and "region" not in dimensions:
            filters.append({"dimension": "region", "operator": "=", "value": detected_region})
        if detected_product and "product" not in dimensions:
            filters.append({"dimension": "product", "operator": "=", "value": detected_product})
        if detected_category and "category" not in dimensions:
            filters.append({"dimension": "category", "operator": "=", "value": detected_category})

        reasoning_steps.append({
            "step": 1,
            "action": "Governed Intent Parsing & Tool Resolution",
            "thought": f"Resolved intent to measures={measures}, dimensions={dimensions}, filters={filters}",
            "query_measures": measures,
            "query_dimensions": dimensions
        })

        return {
            "measures": measures,
            "dimensions": dimensions,
            "filters": filters,
            "limit": 10 if "highest" in prompt_lower or "top" in prompt_lower else 100,
            "order_by": measures[0] if measures else None
        }

    def _execute_resolved_intent(
        self,
        prompt: str,
        intent: Dict[str, Any],
        reasoning_steps: List[Dict[str, Any]],
        start_time: float
    ) -> Dict[str, Any]:
        measures = intent.get("measures", ["revenue"])
        dimensions = intent.get("dimensions", [])
        raw_filters = intent.get("filters", [])
        limit = intent.get("limit", 100)
        order_by = intent.get("order_by")

        # Extract filter values for tool arguments
        region_filter = None
        product_filter = None
        category_filter = None
        for f in raw_filters:
            if f.get("dimension") == "region":
                region_filter = f.get("value")
            elif f.get("dimension") == "product":
                product_filter = f.get("value")
            elif f.get("dimension") == "category":
                category_filter = f.get("value")

        # Dispatch to specific governed LangChain tool
        if dimensions == ["region"]:
            tool_name = "get_sales_by_region"
            res_dict = get_sales_by_region(
                metric=measures[0] if measures else "revenue",
                product=product_filter,
                category=category_filter
            )
        elif dimensions == ["product"]:
            tool_name = "get_sales_by_product"
            res_dict = get_sales_by_product(
                metric=measures[0] if measures else "revenue",
                region=region_filter,
                category=category_filter,
                limit=limit
            )
        elif not dimensions and measures == ["revenue"]:
            tool_name = "get_revenue"
            res_dict = get_revenue(
                region=region_filter,
                product=product_filter,
                category=category_filter
            )
        elif not dimensions and measures == ["cost"]:
            tool_name = "get_cost"
            res_dict = get_cost(
                region=region_filter,
                product=product_filter,
                category=category_filter
            )
        elif not dimensions and measures == ["profit"]:
            tool_name = "get_profit"
            res_dict = get_profit(
                region=region_filter,
                product=product_filter,
                category=category_filter
            )
        elif not dimensions and ("margin" in measures or "margin_pct" in measures):
            tool_name = "get_margin"
            res_dict = get_margin(
                region=region_filter,
                product=product_filter,
                category=category_filter
            )
        elif not dimensions and "customer_count" in measures:
            tool_name = "get_customer_metrics"
            res_dict = get_customer_metrics(
                region=region_filter
            )
        else:
            tool_name = "execute_governed_query"
            res_dict = execute_governed_query(
                measures=measures,
                dimensions=dimensions,
                filters=raw_filters,
                limit=limit,
                order_by=order_by,
                order_desc=True
            )

        filter_objs = [
            FilterCondition(
                dimension=f["dimension"],
                operator=f.get("operator", "="),
                value=f["value"]
            )
            for f in raw_filters
        ]

        reasoning_steps.append({
            "step": 2,
            "action": f"Invoke Governed Tool: {tool_name}",
            "tool_invoked": tool_name,
            "generated_sql": res_dict.get("generated_sql"),
            "row_count": res_dict.get("row_count", 0),
            "observation": f"Retrieved {res_dict.get('row_count', 0)} rows from {res_dict.get('data_source', 'Cube/PostgreSQL')}."
        })

        data = res_dict.get("data", [])
        explanation = self._build_executive_explanation(prompt, measures, dimensions, filter_objs, data)
        chart_config = self._build_chart_config(measures, dimensions, data)

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "query": prompt,
            "status": "success",
            "answer": self._extract_headline_answer(measures, data),
            "metric": measures[0] if measures else "revenue",
            "explanation": explanation,
            "chart_config": chart_config,
            "reasoning_steps": reasoning_steps,
            "transparency": {
                "api_calls": [{"step": 1, "request": {"measures": measures, "dimensions": dimensions, "filters": raw_filters}, "sql": res_dict.get("generated_sql")}],
                "governed_metrics_used": measures,
                "data_source": res_dict.get("data_source", "Cube.dev / PostgreSQL (fct_sales)"),
                "total_rows_scanned": res_dict.get("row_count", 0),
                "execution_time_ms": elapsed_ms
            }
        }

    def _extract_headline_answer(self, measures: List[str], data: List[Dict[str, Any]]) -> str:
        if not data:
            return "No data found."
        first_row = data[0]
        m = measures[0] if measures else "revenue"
        val = first_row.get(m, 0)
        unit = METRICS_DICTIONARY.get(m, {}).get("unit", "")
        if unit == "USD":
            return f"${val:,.2f}"
        elif unit == "percent":
            return f"{val:.2f}%"
        else:
            return f"{val:,}"

    def _build_executive_explanation(
        self,
        query: str,
        measures: List[str],
        dimensions: List[str],
        filters: List[FilterCondition],
        data: List[Dict[str, Any]]
    ) -> str:
        if not data:
            return "### Governed Analytics\n\nNo records found in the data warehouse matching your query criteria."

        measure_labels = [METRICS_DICTIONARY.get(m, {}).get("label", m) for m in measures]
        measures_str = ", ".join(measure_labels)
        filter_str = ", ".join([f"{f.dimension} = '{f.value}'" for f in filters])
        header_suffix = f" (Filters: {filter_str})" if filters else ""

        lines = [f"### Governed Analytics: {measures_str}{header_suffix}\n"]

        if not dimensions and len(data) == 1:
            row = data[0]
            lines.append("Here is the authoritative metric calculation from the governed semantic layer:\n")
            for m in measures:
                val = row.get(m, 0)
                unit = METRICS_DICTIONARY.get(m, {}).get("unit", "")
                label = METRICS_DICTIONARY.get(m, {}).get("label", m)
                formula = METRICS_DICTIONARY.get(m, {}).get("sql_formula", "")
                
                if unit == "USD":
                    formatted = f"${val:,.2f}"
                elif unit == "percent":
                    formatted = f"{val:.2f}%"
                else:
                    formatted = f"{val:,}"
                
                lines.append(f"- **{label}**: **{formatted}** `(Formula: {formula})`")
            return "\n".join(lines)

        lines.append("Here is the breakdown by dimension:\n")
        primary_dim = dimensions[0] if dimensions else "item"

        for idx, row in enumerate(data[:15], 1):
            dim_val = row.get(primary_dim, "Unknown")
            val_strs = []
            for m in measures:
                val = row.get(m, 0)
                unit = METRICS_DICTIONARY.get(m, {}).get("unit", "")
                formatted = f"${val:,.2f}" if unit == "USD" else (f"{val:.2f}%" if unit == "percent" else f"{val:,}")
                val_strs.append(f"{METRICS_DICTIONARY.get(m, {}).get('label', m)}: **{formatted}**")
            lines.append(f"{idx}. **{dim_val}** — {', '.join(val_strs)}")

        if len(data) > 15:
            lines.append(f"\n*(Showing top 15 of {len(data)} total records)*")

        return "\n".join(lines)

    def _build_chart_config(
        self,
        measures: List[str],
        dimensions: List[str],
        data: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        if not data or not dimensions:
            return None

        primary_dim = dimensions[0]
        measure_label = METRICS_DICTIONARY.get(measures[0], {}).get("label", measures[0])
        title = f"{measure_label} by {primary_dim.replace('_', ' ').title()}"

        if primary_dim in ["quarter", "month", "date", "year"]:
            return EChartsBuilder.build_line_chart(title, data, primary_dim, measures)
        elif len(data) <= 6 and len(measures) == 1:
            return EChartsBuilder.build_bar_chart(title, data, primary_dim, measures)
        else:
            return EChartsBuilder.build_bar_chart(title, data, primary_dim, measures)

    def _execute_root_cause_analysis(
        self,
        prompt: str,
        reasoning_steps: List[Dict[str, Any]],
        start_time: float
    ) -> Dict[str, Any]:
        """
        Executes multi-step reasoning for root cause investigation.
        Invokes governed tools to analyze quarterly trends and product category distributions.
        """
        prompt_lower = prompt.lower()
        region = "Europe" if "europe" in prompt_lower else ("Asia" if "asia" in prompt_lower else "North America")

        reasoning_steps.append({
            "step": 1,
            "action": "Plan Root Cause Investigation",
            "thought": f"User requested margin/cost causal analysis in {region}. Multi-step plan:\n1. Invoke tool for quarterly regional trend.\n2. Invoke tool for category cost breakdown.\n3. Synthesize findings."
        })

        # Step 1: Query quarter-by-quarter trend
        res1 = execute_governed_query(
            measures=["revenue", "cost", "profit", "margin_pct"],
            dimensions=["quarter"],
            filters=[{"dimension": "region", "operator": "=", "value": region}],
            limit=20
        )

        reasoning_steps.append({
            "step": 2,
            "action": "Invoke Governed Tool: execute_governed_query (Quarterly Trend)",
            "generated_sql": res1.get("generated_sql"),
            "row_count": res1.get("row_count", 0),
            "observation": f"Retrieved {res1.get('row_count', 0)} quarters of data for {region}."
        })

        # Step 2: Query product category breakdown
        res2 = execute_governed_query(
            measures=["revenue", "cost", "profit", "margin_pct"],
            dimensions=["category"],
            filters=[{"dimension": "region", "operator": "=", "value": region}],
            limit=20
        )

        reasoning_steps.append({
            "step": 3,
            "action": "Invoke Governed Tool: execute_governed_query (Category Breakdown)",
            "generated_sql": res2.get("generated_sql"),
            "row_count": res2.get("row_count", 0),
            "observation": f"Analyzed {res2.get('row_count', 0)} product categories for cost & margin distribution."
        })

        data1 = res1.get("data", [])
        data2 = res2.get("data", [])

        explanation_lines = [
            f"### Root Cause Investigation: {region} Performance & Margin Analysis\n",
            f"Based on governed semantic analytics across {len(data1)} quarters and {len(data2)} product categories in **{region}**:\n",
            "#### 1. Quarterly Performance Trend"
        ]

        for row in data1:
            qtr = row.get("quarter", "")
            rev = row.get("revenue", 0)
            cost = row.get("cost", 0)
            margin_pct = row.get("margin_pct", 0)
            explanation_lines.append(f"- **{qtr}**: Revenue = **${rev:,.2f}** | Cost = **${cost:,.2f}** | Margin = **{margin_pct:.2f}%**")

        explanation_lines.append("\n#### 2. Category Performance & Cost Attribution")
        for row in data2:
            cat = row.get("category", "")
            rev = row.get("revenue", 0)
            profit = row.get("profit", 0)
            margin_pct = row.get("margin_pct", 0)
            explanation_lines.append(f"- **{cat}**: Revenue = **${rev:,.2f}** | Profit = **${profit:,.2f}** | Margin = **{margin_pct:.2f}%**")

        explanation_lines.append(
            f"\n#### 3. Key Findings\n"
            f"- Margin performance across {region} reflects product mix and cost absorption across product categories.\n"
            f"- All values are compiled directly from governed analytical models without hallucination."
        )

        chart_config = EChartsBuilder.build_bar_chart(
            title=f"{region} Quarterly Revenue vs Cost ($)",
            data=data1,
            category_dim="quarter",
            value_cols=["revenue", "cost", "profit"]
        )

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "query": prompt,
            "status": "success",
            "answer": f"{region} Multi-Step Analysis",
            "metric": "margin_pct",
            "explanation": "\n".join(explanation_lines),
            "chart_config": chart_config,
            "reasoning_steps": reasoning_steps,
            "transparency": {
                "api_calls": [
                    {"step": 1, "request": {"measures": ["revenue", "cost", "profit", "margin_pct"], "dimensions": ["quarter"], "filters": [{"dimension": "region", "operator": "=", "value": region}]}, "sql": res1.get("generated_sql")},
                    {"step": 2, "request": {"measures": ["revenue", "cost", "profit", "margin_pct"], "dimensions": ["category"], "filters": [{"dimension": "region", "operator": "=", "value": region}]}, "sql": res2.get("generated_sql")}
                ],
                "governed_metrics_used": ["revenue", "cost", "profit", "margin_pct"],
                "data_source": res1.get("data_source", "Cube.dev / PostgreSQL (fct_sales)"),
                "total_rows_scanned": res1.get("row_count", 0) + res2.get("row_count", 0),
                "execution_time_ms": elapsed_ms
            }
        }

    def _build_clarification_response(
        self,
        prompt: str,
        reasoning_steps: List[Dict[str, Any]],
        start_time: float
    ) -> Dict[str, Any]:
        reasoning_steps.append({
            "step": 1,
            "action": "Governance Guardrail: Metric Whitelist Inspection",
            "thought": "No governed business metric identified in user question. Requesting user clarification."
        })

        metrics_list_md = "\n".join([
            f"- **{v['label']}** (`{k}`): {v['description']}"
            for k, v in METRICS_DICTIONARY.items()
        ])

        explanation = (
            f"### Clarification Required\n\n"
            f"MetricMind could not identify an approved governed business metric in your question: *\"{prompt}\"*.\n\n"
            f"To prevent metric hallucinations, MetricMind only evaluates authoritative business measures.\n\n"
            f"**Available Governed Metrics**:\n"
            f"{metrics_list_md}\n\n"
            f"**Supported Dimensions**: Region, Country, Product, Category, Tier, Customer Segment, Date, Quarter, Month, Year.\n\n"
            f"*Example questions you can ask*:\n"
            f"- *\"How much revenue did we make in Europe?\"*\n"
            f"- *\"Show revenue by region.\"*\n"
            f"- *\"Which product generated the highest revenue?\"*\n"
            f"- *\"What is our profit and margin?\"*"
        )

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "query": prompt,
            "status": "clarification_needed",
            "answer": "Clarification Required",
            "metric": "unsupported",
            "explanation": explanation,
            "chart_config": None,
            "reasoning_steps": reasoning_steps,
            "transparency": {
                "api_calls": [],
                "governed_metrics_used": [],
                "data_source": "Governed Metric Catalog",
                "total_rows_scanned": 0,
                "execution_time_ms": elapsed_ms
            }
        }
