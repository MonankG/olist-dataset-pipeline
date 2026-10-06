select
    order_id,
    order_item_id::int as order_item_id,
    product_id,
    seller_id,
    shipping_limit_date::timestamp_ntz as shipping_limit_date,
    price::float as price,
    freight_value::float as freight_value
from {{ source('raw_olist', 'order_items') }}
