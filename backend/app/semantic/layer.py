"""
Governed Semantic Layer Engine for MetricMind.

Translates structured JSON semantic query definitions into validated, executable SQL
for PostgreSQL. Enforces single business definitions and prevents SQL injection.
"""

import time
import os
import httpx
from typing import List, Dict, Any, Tuple, Optional
from decimal import Decimal

from backend.app.semantic.metadata import METRICS_DICTIONARY, DIMENSIONS_DICTIONARY
from backend.app.semantic.models import SemanticQueryRequest, SemanticQueryResponse, FilterCondition
from backend.database import execute_raw_sql

MAX_ALLOWED_ROWS = 1000
CUBE_API_URL = os.getenv("CUBE_API_URL", "http://localhost:4000/cubejs-api/v1/load")

class SemanticLayerValidationError(Exception):
    pass

class GovernedSemanticEngine:

    @staticmethod
    def validate_request(request: SemanticQueryRequest) -> None:
        """
        Validates measures, dimensions, and filters against the authoritative dictionary.
        Rejects unknown metrics or dimensions.
        """
        if not request.measures:
            raise SemanticLayerValidationError("At least one valid measure must be specified.")

        for m in request.measures:
            if m not in METRICS_DICTIONARY:
                available = ", ".join(METRICS_DICTIONARY.keys())
                raise SemanticLayerValidationError(
                    f"Unknown metric '{m}'. Governed metrics available: {available}"
                )

        if request.dimensions:
            for d in request.dimensions:
                if d not in DIMENSIONS_DICTIONARY:
                    available = ", ".join(DIMENSIONS_DICTIONARY.keys())
                    raise SemanticLayerValidationError(
                        f"Unknown dimension '{d}'. Governed dimensions available: {available}"
                    )

        if request.filters:
            for f in request.filters:
                if f.dimension not in DIMENSIONS_DICTIONARY:
                    available = ", ".join(DIMENSIONS_DICTIONARY.keys())
                    raise SemanticLayerValidationError(
                        f"Filter dimension '{f.dimension}' is not governed. Governed dimensions: {available}"
                    )

    @staticmethod
    def build_sql(request: SemanticQueryRequest) -> Tuple[str, Dict[str, Any]]:
        """
        Compiles a SemanticQueryRequest into a governed, parameterized PostgreSQL query.
        """
        select_clauses = []
        group_clauses = []
        where_clauses = []
        params = {}

        # 1. Dimensions
        if request.dimensions:
            for d_name in request.dimensions:
                sql_col = DIMENSIONS_DICTIONARY[d_name]["sql_column"]
                select_clauses.append(f"{sql_col} AS {d_name}")
                group_clauses.append(sql_col)

        # 2. Measures
        for m_name in request.measures:
            formula = METRICS_DICTIONARY[m_name]["sql_formula"]
            select_clauses.append(f"{formula} AS {m_name}")

        # 3. Filters
        if request.filters:
            for idx, f in enumerate(request.filters):
                sql_col = DIMENSIONS_DICTIONARY[f.dimension]["sql_column"]
                param_key = f"p_{idx}"
                op = str(f.operator).upper().strip()

                if op in ["=", "EQUALS", "EQ"]:
                    where_clauses.append(f"LOWER(CAST({sql_col} AS TEXT)) = LOWER(:{param_key})")
                    params[param_key] = str(f.value)
                elif op in ["!=", "NOT_EQUALS", "NE"]:
                    where_clauses.append(f"LOWER(CAST({sql_col} AS TEXT)) != LOWER(:{param_key})")
                    params[param_key] = str(f.value)
                elif op == "IN" and isinstance(f.value, list):
                    val_keys = []
                    for v_idx, v in enumerate(f.value):
                        vk = f"{param_key}_{v_idx}"
                        val_keys.append(f":{vk}")
                        params[vk] = str(v).lower()
                    in_clause = ", ".join(val_keys)
                    where_clauses.append(f"LOWER(CAST({sql_col} AS TEXT)) IN ({in_clause})")
                elif op in [">=", "GTE"]:
                    where_clauses.append(f"{sql_col} >= :{param_key}")
                    params[param_key] = str(f.value)
                elif op in ["<=", "LTE"]:
                    where_clauses.append(f"{sql_col} <= :{param_key}")
                    params[param_key] = str(f.value)
                elif op == "LIKE":
                    where_clauses.append(f"LOWER(CAST({sql_col} AS TEXT)) LIKE LOWER(:{param_key})")
                    params[param_key] = f"%{str(f.value)}%"
                else:
                    where_clauses.append(f"LOWER(CAST({sql_col} AS TEXT)) = LOWER(:{param_key})")
                    params[param_key] = str(f.value)

        # 4. Construct Full SQL with Standard Left Joins
        select_str = ",\n    ".join(select_clauses)
        sql = (
            f"SELECT\n    {select_str}\n"
            f"FROM sales s\n"
            f"LEFT JOIN products p ON s.product_id = p.product_id\n"
            f"LEFT JOIN customers c ON s.customer_id = c.customer_id\n"
            f"LEFT JOIN customer_status cs ON s.customer_id = cs.customer_id"
        )

        if where_clauses:
            where_str = "\n  AND ".join(where_clauses)
            sql += f"\nWHERE {where_str}"

        if group_clauses:
            group_str = ", ".join(group_clauses)
            sql += f"\nGROUP BY {group_str}"

        # 5. Order By
        if request.order_by and (request.order_by in request.measures or request.order_by in request.dimensions):
            direction = "DESC" if request.order_desc else "ASC"
            sql += f"\nORDER BY {request.order_by} {direction}"
        elif request.dimensions:
            # Default order by first measure descending or first dimension
            if request.measures:
                sql += f"\nORDER BY {request.measures[0]} DESC"
            else:
                sql += f"\nORDER BY {group_clauses[0]} ASC"

        limit = min(request.limit or 100, MAX_ALLOWED_ROWS)
        sql += f"\nLIMIT {limit};"

        return sql, params

    @classmethod
    def execute_query(cls, request: SemanticQueryRequest) -> SemanticQueryResponse:
        """
        Validates, compiles, and runs the semantic query against PostgreSQL.
        """
        start_time = time.time()
        try:
            cls.validate_request(request)
            sql, params = cls.build_sql(request)

            raw_rows, columns = execute_raw_sql(sql, params)

            # Sanitize Decimal and numeric types for clean JSON response
            sanitized_rows = []
            for row in raw_rows:
                clean_row = {}
                for k, v in row.items():
                    if isinstance(v, Decimal):
                        clean_row[k] = float(v)
                    else:
                        clean_row[k] = v
                sanitized_rows.append(clean_row)

            elapsed_ms = round((time.time() - start_time) * 1000, 2)

            return SemanticQueryResponse(
                status="success",
                measures=request.measures,
                dimensions=request.dimensions or [],
                generated_sql=sql,
                data=sanitized_rows,
                row_count=len(sanitized_rows),
                execution_time_ms=elapsed_ms,
                governance_passed=True,
                data_source="PostgreSQL (metricmind)"
            )

        except SemanticLayerValidationError as ve:
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            return SemanticQueryResponse(
                status="error",
                measures=request.measures,
                dimensions=request.dimensions or [],
                generated_sql="",
                data=[],
                row_count=0,
                execution_time_ms=elapsed_ms,
                governance_passed=False,
                data_source="PostgreSQL (metricmind)",
                error_message=str(ve)
            )
        except Exception as e:
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            return SemanticQueryResponse(
                status="error",
                measures=request.measures,
                dimensions=request.dimensions or [],
                generated_sql="",
                data=[],
                row_count=0,
                execution_time_ms=elapsed_ms,
                governance_passed=False,
                data_source="PostgreSQL (metricmind)",
                error_message=f"PostgreSQL Execution Error: {str(e)}"
            )
