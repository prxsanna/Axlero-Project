-- Staging model for customer status
with source as (
    select
        customer_id,
        purchase_count,
        last_purchase_date,
        churn_status
    from customer_status
)

select * from source
