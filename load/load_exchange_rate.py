"""
Loads exchange rate CSVs from S3 into Snowflake (schema RAW), one file per
day. Unlike load_to_snowflake.py, this uses CREATE TABLE IF NOT EXISTS (not
CREATE OR REPLACE) and lets COPY INTO run against every file in the stage
each time - Snowflake automatically skips files it has already loaded, so
re-running only picks up new days. This is what makes it incremental.
"""

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

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = "raw/exchange_rate"

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    private_key=private_key_bytes,
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)
cur = conn.cursor()

database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

cur.execute(f"USE WAREHOUSE {warehouse}")
cur.execute(f"USE DATABASE {database}")
cur.execute(f"USE SCHEMA {schema}")

cur.execute(
    """
    CREATE FILE FORMAT IF NOT EXISTS CSV_FORMAT
    TYPE = CSV
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    """
)

cur.execute(
    f"""
    CREATE STAGE IF NOT EXISTS EXCHANGE_RATE_STAGE
    URL = 's3://{S3_BUCKET}/{S3_PREFIX}/'
    CREDENTIALS = (
        AWS_KEY_ID = '{os.getenv("AWS_ACCESS_KEY_ID")}'
        AWS_SECRET_KEY = '{os.getenv("AWS_SECRET_ACCESS_KEY")}'
    )
    FILE_FORMAT = CSV_FORMAT
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS EXCHANGE_RATE (
        date VARCHAR,
        usd_to_brl_rate VARCHAR
    )
    """
)

cur.execute("COPY INTO EXCHANGE_RATE FROM @EXCHANGE_RATE_STAGE")
columns = [d[0] for d in cur.description]
for row in cur.fetchall():
    print(dict(zip(columns, row)))

cur.close()
conn.close()
print("Done.")
