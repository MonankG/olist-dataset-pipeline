"""
Downloads the Olist dataset from Kaggle and uploads the raw CSVs to S3, untouched.
"""

import os

import boto3
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

load_dotenv()

DATASET = "olistbr/brazilian-ecommerce"
LOCAL_DIR = os.path.join(os.path.dirname(__file__), "data")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = "raw/olist"

# 1. Download the dataset from Kaggle
api = KaggleApi()
api.authenticate()

os.makedirs(LOCAL_DIR, exist_ok=True)
api.dataset_download_files(DATASET, path=LOCAL_DIR, unzip=True)

# 2. Upload each CSV to S3, untouched
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

for filename in os.listdir(LOCAL_DIR):
    if not filename.endswith(".csv"):
        continue

    local_path = os.path.join(LOCAL_DIR, filename)
    s3_key = f"{S3_PREFIX}/{filename}"

    print(f"Uploading {filename} -> s3://{S3_BUCKET}/{s3_key}")
    s3.upload_file(local_path, S3_BUCKET, s3_key)

print("Done.")
