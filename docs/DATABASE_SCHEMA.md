# MetricMind — PostgreSQL Database Schema

This document details the authoritative database schema for MetricMind.

---

## 1. Relational Tables

### 1.1 `sales`
Primary transaction table containing 50,000 historical sales orders from 2024 to 2025.

| Column | Data Type | Description |
|---|---|---|
| `sale_id` | `VARCHAR(20)` | Primary Key (e.g. `SALE000001`) |
| `sale_date` | `DATE` | Transaction timestamp |
| `customer_id` | `VARCHAR(20)` | Foreign Key to `customers.customer_id` |
| `product_id` | `VARCHAR(20)` | Foreign Key to `products.product_id` |
| `region` | `VARCHAR(100)` | Sales region (`Asia`, `Europe`, `North America`, `Oceania`, `South America`) |
| `quantity` | `INTEGER` | Quantity of items purchased |
| `unit_price` | `NUMERIC(12, 2)` | Standard unit price at sale |
| `discount` | `NUMERIC(5, 2)` | Applied discount percentage (e.g. `0.05`) |
| `revenue` | `NUMERIC(12, 2)` | Total sales dollar revenue |
| `cost` | `NUMERIC(12, 2)` | Total order cost |
| `profit` | `NUMERIC(12, 2)` | Operating dollar profit (`revenue - cost`) |
| `margin` | `NUMERIC(8, 2)` | Operating margin ratio |

---

### 1.2 `products`
Catalog of 20 software, cloud, analytics, and security products.

| Column | Data Type | Description |
|---|---|---|
| `product_id` | `VARCHAR(20)` | Primary Key (e.g. `PROD001`) |
| `product_name` | `VARCHAR(100)` | Product name (e.g. `Analytics Pro`, `Cloud Enterprise`) |
| `category` | `VARCHAR(100)` | Product category (`Analytics`, `Cloud`, `Security`, `CRM`, `Data Platform`, `AI`, `Support`) |
| `tier` | `VARCHAR(50)` | Product tier (`Basic`, `Pro`, `Enterprise`, `Standard`, `Premium`) |
| `monthly_price` | `NUMERIC(12, 2)` | Base monthly catalog price |

---

### 1.3 `customers`
10,000 registered business customers across 18 countries.

| Column | Data Type | Description |
|---|---|---|
| `customer_id` | `VARCHAR(20)` | Primary Key (e.g. `CUST00001`) |
| `customer_name` | `VARCHAR(100)` | Customer business name |
| `country` | `VARCHAR(100)` | Customer country |
| `region` | `VARCHAR(100)` | Global geographic region |
| `customer_segment` | `VARCHAR(50)` | Business segment (`SMB`, `Mid-Market`, `Enterprise`) |
| `signup_date` | `DATE` | Account registration date |
| `acquisition_channel` | `VARCHAR(50)` | Marketing acquisition channel (`Organic`, `Paid Search`, `Social`, `Partner`, `Referral`) |

---

### 1.4 `customer_status`
Customer lifecycle, purchase frequency, and churn tracking for 10,000 customers.

| Column | Data Type | Description |
|---|---|---|
| `customer_id` | `VARCHAR(20)` | Primary Key / Foreign Key to `customers.customer_id` |
| `purchase_count` | `INTEGER` | Lifetime transaction frequency |
| `last_purchase_date` | `DATE` | Most recent transaction date |
| `churn_status` | `VARCHAR(30)` | Churn categorization (`Active`, `Churned`) |

---

## 2. Governed Fact Mart: `fct_sales`

Compiled via dbt or joined directly in the semantic layer:

```sql
SELECT
    s.sale_id as order_id,
    s.sale_date as order_date,
    EXTRACT(YEAR FROM s.sale_date)::integer as year,
    CONCAT('Q', EXTRACT(QUARTER FROM s.sale_date)::integer, ' ', EXTRACT(YEAR FROM s.sale_date)::integer) as quarter,
    TO_CHAR(s.sale_date, 'YYYY-MM') as month,
    s.region,
    c.country,
    p.product_name as product,
    p.category,
    p.tier,
    c.customer_segment,
    s.quantity,
    s.revenue,
    s.cost,
    ROUND((s.cost * 0.75)::numeric, 2) as material_cost,
    ROUND((s.cost * 0.25)::numeric, 2) as shipping_cost,
    s.profit as margin,
    CASE WHEN s.revenue > 0 THEN ROUND(((s.profit / s.revenue) * 100.0)::numeric, 2) ELSE 0.0 END as margin_pct
FROM sales s
LEFT JOIN products p ON s.product_id = p.product_id
LEFT JOIN customers c ON s.customer_id = c.customer_id;
```
