-- Grain: one row per order item (order_id + order_item_id). This is what
-- lets the fact join to dim_products and dim_sellers, since an order can
-- contain items from multiple products/sellers.
--
-- order_status, the delivery dates, and review_score are order-level
-- attributes, duplicated across an order's items - fine to display per row,
-- but must NOT be summed across items of the same order (that would double
-- count). price and freight_value are genuine item-level measures and are
-- safe to sum.
select
    oi.order_id,
    oi.order_item_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,
    date(o.order_purchase_timestamp) as order_purchase_date,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    datediff('day', o.order_purchase_timestamp, o.order_delivered_customer_date) as delivery_days,
    datediff('day', o.order_delivered_customer_date, o.order_estimated_delivery_date) as delivery_vs_estimate_days,
    oi.price,
    oi.freight_value,
    r.review_score
from {{ ref('stg_order_items') }} oi
left join {{ ref('stg_orders') }} o on oi.order_id = o.order_id
left join (
    select order_id, avg(review_score) as review_score
    from {{ ref('stg_order_reviews') }}
    group by order_id
) r on oi.order_id = r.order_id
