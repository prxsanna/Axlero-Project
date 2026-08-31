-- Staging model for raw sales data
with source as (
    select
        sale_id,
        sale_date,
        customer_id,
        product_id,
        region,
        quantity,
        unit_price,
        discount,
        revenue,
        cost,
        profit,
        margin
    from sales
)

select * from source
