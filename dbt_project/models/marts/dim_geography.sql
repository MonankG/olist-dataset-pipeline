-- The raw geolocation data has many lat/lng points per zip code prefix (and
-- occasional city/state spelling variants for the same prefix). Collapsed to
-- one row per zip: average lat/lng, and MIN() to deterministically pick a
-- single city/state label.
select
    geolocation_zip_code_prefix as zip_code_prefix,
    min(geolocation_city) as city,
    min(geolocation_state) as state,
    avg(geolocation_lat) as latitude,
    avg(geolocation_lng) as longitude
from {{ ref('stg_geolocation') }}
group by geolocation_zip_code_prefix
