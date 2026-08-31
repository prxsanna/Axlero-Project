-- Staging model for products dimension
with source as (
    select
        product_id,
        product_name,
        category,
        tier,
        monthly_price
    from products
)

select * from source
