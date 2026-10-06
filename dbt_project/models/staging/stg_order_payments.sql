select
    order_id,
    payment_sequential::int as payment_sequential,
    payment_type,
    payment_installments::int as payment_installments,
    payment_value::float as payment_value
from {{ source('raw_olist', 'order_payments') }}
