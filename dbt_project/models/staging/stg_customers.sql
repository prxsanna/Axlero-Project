-- Staging model for customers dimension
with source as (
    select
        customer_id,
        customer_name,
        country,
        region,
        customer_segment,
        signup_date,
        acquisition_channel
    from customers
)

select * from source
