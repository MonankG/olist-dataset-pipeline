-- Calendar spine covering the Olist dataset's date range (orders run
-- 2016-2018). Built with Snowflake's GENERATOR table function instead of a
-- dbt package, to avoid an extra dependency for one simple table.
with date_spine as (
    select dateadd('day', seq4(), '2016-01-01'::date) as date_day
    from table(generator(rowcount => 1500))
)
select
    date_day,
    year(date_day) as year,
    month(date_day) as month,
    day(date_day) as day,
    dayofweek(date_day) as day_of_week,
    dayname(date_day) as day_name,
    quarter(date_day) as quarter
from date_spine
