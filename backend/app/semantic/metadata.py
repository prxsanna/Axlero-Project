"""
Authoritative Governed Metric & Dimension Definitions for MetricMind.

Rule: Single source of truth for business definitions.
Metrics must have one authoritative formula and mapping.
"""

from typing import Dict, Any

METRICS_DICTIONARY: Dict[str, Dict[str, Any]] = {
    "revenue": {
        "name": "revenue",
        "label": "Revenue",
        "description": "Total gross sales revenue ($)",
        "sql_formula": "SUM(s.revenue)",
        "unit": "USD",
        "format": "currency"
    },
    "cost": {
        "name": "cost",
        "label": "Total Cost",
        "description": "Total cost associated with sales ($)",
        "sql_formula": "SUM(s.cost)",
        "unit": "USD",
        "format": "currency"
    },
    "profit": {
        "name": "profit",
        "label": "Operating Profit",
        "description": "Net dollar profit: SUM(s.revenue - s.cost)",
        "sql_formula": "SUM(s.profit)",
        "unit": "USD",
        "format": "currency"
    },
    "margin": {
        "name": "margin",
        "label": "Operating Margin ($)",
        "description": "Net operating dollar margin: SUM(s.profit)",
        "sql_formula": "SUM(s.profit)",
        "unit": "USD",
        "format": "currency"
    },
    "margin_pct": {
        "name": "margin_pct",
        "label": "Margin Percentage",
        "description": "Operating margin percentage: (SUM(profit) / SUM(revenue)) * 100",
        "sql_formula": "CASE WHEN SUM(s.revenue) > 0 THEN ROUND((SUM(s.profit) / SUM(s.revenue) * 100.0)::numeric, 2) ELSE 0.0 END",
        "unit": "percent",
        "format": "percentage"
    },
    "quantity": {
        "name": "quantity",
        "label": "Quantity Sold",
        "description": "Total units sold across orders",
        "sql_formula": "SUM(s.quantity)",
        "unit": "units",
        "format": "number"
    },
    "customer_count": {
        "name": "customer_count",
        "label": "Active Customer Count",
        "description": "Count of unique transacting customers",
        "sql_formula": "COUNT(DISTINCT s.customer_id)",
        "unit": "customers",
        "format": "number"
    },
    "material_cost": {
        "name": "material_cost",
        "label": "Material Cost",
        "description": "Direct material component cost ($)",
        "sql_formula": "SUM(ROUND((s.cost * 0.75)::numeric, 2))",
        "unit": "USD",
        "format": "currency"
    },
    "shipping_cost": {
        "name": "shipping_cost",
        "label": "Shipping Cost",
        "description": "Freight & logistics shipping cost ($)",
        "sql_formula": "SUM(ROUND((s.cost * 0.25)::numeric, 2))",
        "unit": "USD",
        "format": "currency"
    },
    "transaction_count": {
        "name": "transaction_count",
        "label": "Transaction Count",
        "description": "Total number of sales transactions",
        "sql_formula": "COUNT(s.sale_id)",
        "unit": "orders",
        "format": "number"
    }
}

DIMENSIONS_DICTIONARY: Dict[str, Dict[str, Any]] = {
    "date": {
        "name": "date",
        "label": "Sale Date",
        "sql_column": "s.sale_date",
        "type": "time"
    },
    "year": {
        "name": "year",
        "label": "Year",
        "sql_column": "EXTRACT(YEAR FROM s.sale_date)::integer",
        "type": "integer"
    },
    "quarter": {
        "name": "quarter",
        "label": "Quarter",
        "sql_column": "CONCAT('Q', EXTRACT(QUARTER FROM s.sale_date)::integer, ' ', EXTRACT(YEAR FROM s.sale_date)::integer)",
        "type": "string"
    },
    "month": {
        "name": "month",
        "label": "Month",
        "sql_column": "TO_CHAR(s.sale_date, 'YYYY-MM')",
        "type": "string"
    },
    "region": {
        "name": "region",
        "label": "Sales Region",
        "sql_column": "s.region",
        "type": "string"
    },
    "country": {
        "name": "country",
        "label": "Customer Country",
        "sql_column": "c.country",
        "type": "string"
    },
    "product": {
        "name": "product",
        "label": "Product Name",
        "sql_column": "p.product_name",
        "type": "string"
    },
    "category": {
        "name": "category",
        "label": "Product Category",
        "sql_column": "p.category",
        "type": "string"
    },
    "tier": {
        "name": "tier",
        "label": "Product Tier",
        "sql_column": "p.tier",
        "type": "string"
    },
    "customer_segment": {
        "name": "customer_segment",
        "label": "Customer Segment",
        "sql_column": "c.customer_segment",
        "type": "string"
    },
    "acquisition_channel": {
        "name": "acquisition_channel",
        "label": "Acquisition Channel",
        "sql_column": "c.acquisition_channel",
        "type": "string"
    },
    "churn_status": {
        "name": "churn_status",
        "label": "Customer Churn Status",
        "sql_column": "cs.churn_status",
        "type": "string"
    }
}
