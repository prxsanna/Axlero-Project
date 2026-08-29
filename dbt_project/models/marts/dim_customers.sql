-- Customers Dimension Model with Churn Enrichment
with stg_customers as (
    select * from {{ ref('stg_customers') }}
),
stg_status as (
    select * from {{ ref('stg_customer_status') }}
)

select
    c.customer_id,
    c.customer_name,
    c.country,
    c.region,
    c.customer_segment,
    c.signup_date,
    c.acquisition_channel,
    coalesce(s.purchase_count, 0) as purchase_count,
    s.last_purchase_date,
    coalesce(s.churn_status, 'Active') as churn_status
from stg_customers c
left join stg_status s on c.customer_id = s.customer_id
