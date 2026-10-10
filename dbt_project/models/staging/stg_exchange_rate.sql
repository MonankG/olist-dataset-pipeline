select
    date::date as rate_date,
    usd_to_brl_rate::float as usd_to_brl_rate
from {{ source('raw_olist', 'exchange_rate') }}
