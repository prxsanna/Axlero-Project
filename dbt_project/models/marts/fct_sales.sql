-- Governed Analytical Mart for MetricMind Sales, Cost, and Profit
with stg_sales as (
    select * from {{ ref('stg_sales') }}
),
stg_products as (
    select * from {{ ref('stg_products') }}
),
stg_customers as (
    select * from {{ ref('stg_customers') }}
)

select
    s.sale_id as order_id,
    s.sale_date as order_date,
    extract(year from s.sale_date::date)::integer as year,
    concat('Q', extract(quarter from s.sale_date::date)::integer, ' ', extract(year from s.sale_date::date)::integer) as quarter,
    to_char(s.sale_date::date, 'YYYY-MM') as month,
    s.customer_id,
    c.customer_name,
    c.country,
    s.region,
    c.customer_segment,
    s.product_id,
    p.product_name as product,
    p.category,
    p.tier,
    s.quantity,
    s.unit_price,
    s.discount,
    s.revenue,
    s.cost,
    round((s.cost * 0.75)::numeric, 2) as material_cost,
    round((s.cost * 0.25)::numeric, 2) as shipping_cost,
    s.profit as margin,
    case
        when s.revenue > 0 then round(((s.profit / s.revenue) * 100.0)::numeric, 2)
        else 0.0
    end as margin_pct
from stg_sales s
left join stg_products p on s.product_id = p.product_id
left join stg_customers c on s.customer_id = c.customer_id
