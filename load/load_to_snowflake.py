"""
Loads the raw Olist CSVs from S3 into Snowflake staging tables (schema RAW).

Snowflake reads directly from S3 via an external stage - the CSVs are not
downloaded again here. Column names are read from the local copies in
extract/data/ (left over from the extract step) just to build the CREATE TABLE
statements; every column is loaded as VARCHAR since this is the raw layer -
type casting/cleaning happens later in dbt staging models.
"""

import csv
import os

import snowflake.connector
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "keys", "rsa_key.p8")
with open(PRIVATE_KEY_PATH, "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None)

private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

LOCAL_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "extract", "data")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = "raw/olist"

# csv filename -> Snowflake table name
TABLES = {
    "olist_customers_dataset.csv": "CUSTOMERS",
    "olist_geolocation_dataset.csv": "GEOLOCATION",
    "olist_order_items_dataset.csv": "ORDER_ITEMS",
    "olist_order_payments_dataset.csv": "ORDER_PAYMENTS",
    "olist_order_reviews_dataset.csv": "ORDER_REVIEWS",
    "olist_orders_dataset.csv": "ORDERS",
    "olist_products_dataset.csv": "PRODUCTS",
    "olist_sellers_dataset.csv": "SELLERS",
    "product_category_name_translation.csv": "PRODUCT_CATEGORY_NAME_TRANSLATION",
}

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    private_key=private_key_bytes,
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)
cur = conn.cursor()

# 0. Make sure the database/schema/warehouse actually exist and are active
#    for this session (a fresh Snowflake account won't have them yet).
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

cur.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
cur.execute(f"CREATE SCHEMA IF NOT EXISTS {database}.{schema}")
cur.execute(f"USE WAREHOUSE {warehouse}")
cur.execute(f"USE DATABASE {database}")
cur.execute(f"USE SCHEMA {schema}")

# 1. File format for the raw CSVs
cur.execute(
    """
    CREATE FILE FORMAT IF NOT EXISTS CSV_FORMAT
    TYPE = CSV
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    """
)

# 2. External stage pointing at the S3 prefix where the raw CSVs live
cur.execute(
    f"""
    CREATE STAGE IF NOT EXISTS OLIST_STAGE
    URL = 's3://{S3_BUCKET}/{S3_PREFIX}/'
    CREDENTIALS = (
        AWS_KEY_ID = '{os.getenv("AWS_ACCESS_KEY_ID")}'
        AWS_SECRET_KEY = '{os.getenv("AWS_SECRET_ACCESS_KEY")}'
    )
    FILE_FORMAT = CSV_FORMAT
    """
)

# 3. Create each table (all VARCHAR) and copy its CSV in from the stage
for filename, table_name in TABLES.items():
    local_path = os.path.join(LOCAL_DATA_DIR, filename)
    with open(local_path, encoding="utf-8-sig") as f:
        columns = next(csv.reader(f))

    column_defs = ", ".join(f"{col} VARCHAR" for col in columns)
    cur.execute(f"CREATE OR REPLACE TABLE {table_name} ({column_defs})")

    cur.execute(f"COPY INTO {table_name} FROM @OLIST_STAGE/{filename}")
    result = cur.fetchall()
    rows_loaded = sum(row[3] for row in result)
    print(f"{table_name}: loaded {rows_loaded} rows from {filename}")

cur.close()
conn.close()
print("Done.")
