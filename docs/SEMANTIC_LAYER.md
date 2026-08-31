# MetricMind — Semantic Layer Guide

The Semantic Layer provides a centralized, authoritative layer of business definitions between the AI reasoning layer and the underlying PostgreSQL database.

---

## 1. Why a Semantic Layer is Critical

In raw LLM-to-SQL architectures, models frequently hallucinate conflicting metric formulas:
- LLM A might calculate Margin as `(Revenue - Cost) / Revenue * 100`
- LLM B might calculate Margin as `(Revenue - Material_Cost) / Revenue * 100`
- LLM C might calculate Margin as `Revenue - Cost`

The MetricMind Semantic Layer solves this by defining metric logic once centrally.

---

## 2. Authoritative Metric Definitions

| Metric Key | Label | Formula | Description |
|---|---|---|---|
| `revenue` | Revenue | `SUM(f.revenue)` | Gross sales revenue ($) |
| `cost` | Total Cost | `SUM(f.cost)` | Total operational cost ($) |
| `profit` | Operating Profit | `SUM(f.profit)` | Net operating profit ($) |
| `margin` | Operating Margin | `SUM(f.profit)` | Net operating dollar margin ($) |
| `margin_pct` | Margin Percentage | `(SUM(profit) / SUM(revenue)) * 100` | Net margin percentage (%) |
| `quantity` | Quantity Sold | `SUM(f.quantity)` | Total units sold |
| `customer_count` | Customer Count | `COUNT(DISTINCT f.customer_id)` | Unique transacting customers |
| `material_cost` | Material Cost | `SUM(ROUND(f.cost * 0.75, 2))` | Material & components cost |
| `shipping_cost` | Shipping Cost | `SUM(ROUND(f.cost * 0.25, 2))` | Logistics & freight cost |

---

## 3. Cube.dev Implementation

Cube defines these metrics in `cube/model/cubes/sales.yml` and exposes REST, SQL, and GraphQL APIs.

### Example Cube REST API Payload:
```json
{
  "measures": ["sales.revenue", "sales.margin_pct"],
  "dimensions": ["sales.region"],
  "order": { "sales.revenue": "desc" }
}
```
