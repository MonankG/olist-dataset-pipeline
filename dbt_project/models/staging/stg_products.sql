select
    product_id,
    product_category_name,
    product_name_lenght::int as product_name_length,
    product_description_lenght::int as product_description_length,
    product_photos_qty::int as product_photos_qty,
    product_weight_g::float as product_weight_g,
    product_length_cm::float as product_length_cm,
    product_height_cm::float as product_height_cm,
    product_width_cm::float as product_width_cm
from {{ source('raw_olist', 'products') }}
