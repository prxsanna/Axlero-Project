"""
Authoritative Governed Metric & Dimension Definitions for MetricMind.

Rule: Single source of truth for business definitions.
Metrics must have one authoritative formula and mapping to dbt marts / Cube.dev.
"""

from typing import Dict, Any

METRICS_DICTIONARY: Dict[str, Dict[str, Any]] = {
    "revenue": {
        "name": "revenue",
        "label": "Revenue",
        "description": "Total gross sales revenue ($)",
        "sql_formula": "SUM(f.revenue)",
        "unit": "USD",
        "format": "currency",
        "cube_measure": "sales.revenue"
    },
    "cost": {
        "name": "cost",
        "label": "Total Cost",
        "description": "Total cost associated with sales ($)",
        "sql_formula": "SUM(f.cost)",
        "unit": "USD",
        "format": "currency",
        "cube_measure": "sales.cost"
    },
    "profit": {
        "name": "profit",
        "label": "Operating Profit",
        "description": "Net dollar profit: SUM(f.revenue - f.cost)",
        "sql_formula": "SUM(f.profit)",
        "unit": "USD",
        "format": "currency",
        "cube_measure": "sales.profit"
    },
    "margin": {
        "name": "margin",
        "label": "Operating Margin ($)",
        "description": "Net operating dollar margin: SUM(f.profit)",
        "sql_formula": "SUM(f.profit)",
        "unit": "USD",
        "format": "currency",
        "cube_measure": "sales.margin"
    },
    "margin_pct": {
        "name": "margin_pct",
        "label": "Margin Percentage",
        "description": "Operating margin percentage: (SUM(profit) / SUM(revenue)) * 100",
        "sql_formula": "CASE WHEN SUM(f.revenue) > 0 THEN ROUND((SUM(f.profit) / SUM(f.revenue) * 100.0)::numeric, 2) ELSE 0.0 END",
        "unit": "percent",
        "format": "percentage",
        "cube_measure": "sales.margin_pct"
    },
    "quantity": {
        "name": "quantity",
        "label": "Quantity Sold",
        "description": "Total units sold across orders",
        "sql_formula": "SUM(f.quantity)",
        "unit": "units",
        "format": "number",
        "cube_measure": "sales.quantity"
    },
    "customer_count": {
        "name": "customer_count",
        "label": "Active Customer Count",
        "description": "Count of unique transacting customers",
        "sql_formula": "COUNT(DISTINCT f.customer_id)",
        "unit": "customers",
        "format": "number",
        "cube_measure": "sales.customer_count"
    },
    "material_cost": {
        "name": "material_cost",
        "label": "Material Cost",
        "description": "Direct material component cost ($)",
        "sql_formula": "SUM(ROUND((f.cost * 0.75)::numeric, 2))",
        "unit": "USD",
        "format": "currency",
        "cube_measure": "sales.material_cost"
    },
    "shipping_cost": {
        "name": "shipping_cost",
        "label": "Shipping Cost",
        "description": "Freight & logistics shipping cost ($)",
        "sql_formula": "SUM(ROUND((f.cost * 0.25)::numeric, 2))",
        "unit": "USD",
        "format": "currency",
        "cube_measure": "sales.shipping_cost"
    },
    "transaction_count": {
        "name": "transaction_count",
        "label": "Transaction Count",
        "description": "Total number of sales transactions",
        "sql_formula": "COUNT(f.sale_id)",
        "unit": "orders",
        "format": "number",
        "cube_measure": "sales.transaction_count"
    }
}

DIMENSIONS_DICTIONARY: Dict[str, Dict[str, Any]] = {
    "date": {
        "name": "date",
        "label": "Sale Date",
        "sql_column": "f.sale_date",
        "type": "time",
        "cube_dimension": "sales.date"
    },
    "year": {
        "name": "year",
        "label": "Year",
        "sql_column": "f.year",
        "type": "integer",
        "cube_dimension": "sales.year"
    },
    "quarter": {
        "name": "quarter",
        "label": "Quarter",
        "sql_column": "f.quarter",
        "type": "string",
        "cube_dimension": "sales.quarter"
    },
    "month": {
        "name": "month",
        "label": "Month",
        "sql_column": "f.month",
        "type": "string",
        "cube_dimension": "sales.month"
    },
    "region": {
        "name": "region",
        "label": "Sales Region",
        "sql_column": "f.region",
        "type": "string",
        "cube_dimension": "sales.region"
    },
    "country": {
        "name": "country",
        "label": "Customer Country",
        "sql_column": "f.country",
        "type": "string",
        "cube_dimension": "sales.country"
    },
    "product": {
        "name": "product",
        "label": "Product Name",
        "sql_column": "f.product",
        "type": "string",
        "cube_dimension": "sales.product"
    },
    "category": {
        "name": "category",
        "label": "Product Category",
        "sql_column": "f.category",
        "type": "string",
        "cube_dimension": "sales.category"
    },
    "tier": {
        "name": "tier",
        "label": "Product Tier",
        "sql_column": "f.tier",
        "type": "string",
        "cube_dimension": "sales.tier"
    },
    "customer_segment": {
        "name": "customer_segment",
        "label": "Customer Segment",
        "sql_column": "f.customer_segment",
        "type": "string",
        "cube_dimension": "sales.customer_segment"
    },
    "customer_name": {
        "name": "customer_name",
        "label": "Customer Name",
        "sql_column": "f.customer_name",
        "type": "string",
        "cube_dimension": "sales.customer_name"
    },
    "acquisition_channel": {
        "name": "acquisition_channel",
        "label": "Acquisition Channel",
        "sql_column": "f.acquisition_channel",
        "type": "string",
        "cube_dimension": "sales.acquisition_channel"
    },
    "churn_status": {
        "name": "churn_status",
        "label": "Customer Churn Status",
        "sql_column": "dc.churn_status",
        "type": "string",
        "cube_dimension": "sales.churn_status"
    }
}
