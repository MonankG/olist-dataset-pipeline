"""
Fetches today's USD -> BRL exchange rate and uploads it to S3 as one small
CSV per day. Run daily (via the Airflow DAG), this demonstrates recurring
ingestion rather than a one-time load - each run adds a new, distinctly
named file; Snowflake's COPY INTO skips files it has already loaded, so
re-running never duplicates data.
"""

import csv
import os

import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.frankfurter.app/latest?from=USD&to=BRL"
LOCAL_DIR = os.path.join(os.path.dirname(__file__), "data", "exchange_rate")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = "raw/exchange_rate"

response = requests.get(API_URL, timeout=30)
response.raise_for_status()
data = response.json()

rate_date = data["date"]
usd_to_brl_rate = data["rates"]["BRL"]

os.makedirs(LOCAL_DIR, exist_ok=True)
filename = f"{rate_date}.csv"
local_path = os.path.join(LOCAL_DIR, filename)

with open(local_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "usd_to_brl_rate"])
    writer.writerow([rate_date, usd_to_brl_rate])

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

s3_key = f"{S3_PREFIX}/{filename}"
print(f"Uploading {filename} -> s3://{S3_BUCKET}/{s3_key}")
s3.upload_file(local_path, S3_BUCKET, s3_key)

print("Done.")
