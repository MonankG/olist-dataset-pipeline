# Project Context: Olist E-Commerce Data Pipeline

## Background
I'm a student graduating Spring 2027, targeting Data Engineer, Data Analyst, Data 
Scientist, Software Engineer, and Automation roles. I researched 100 real entry-level 
job listings and analyzed required/preferred skills by category (Data / Automation / 
Both). This project is "Flagship Project 1" — designed to demonstrate Data Engineering 
skills specifically, and is built to feed directly into a "Flagship Project 2" 
(statistical analysis / ML / dashboard) that will query this project's output.

## Top skills this project must demonstrate (from job market research)
Python, SQL, ETL, Data Modeling, Data Warehousing, dbt, Airflow, Git, AWS, Snowflake, 
Data Governance — these were the highest-frequency required/preferred skills across 
Data Engineer job postings in my research.

## What the project is
Using the real, public **Olist Brazilian E-Commerce dataset** (Kaggle: 
`olistbr/brazilian-ecommerce`, ~100K orders, 9 relational CSVs: orders, order_items, 
order_payments, order_reviews, products, customers, sellers, geolocation, 
category_name_translation).

Goal: build an end-to-end pipeline that takes the raw scattered CSVs and turns them 
into a clean, modeled, tested, orchestrated data warehouse — the same kind of system 
a real e-commerce company would use to answer questions like "what's our revenue 
trend," "which categories have the worst delivery times," "does late delivery 
correlate with bad reviews."

## Architecture (Medallion: Bronze → Silver → Gold)
1. **Bronze (raw):** Python script pulls raw CSVs via Kaggle API, lands them 
   untouched in AWS S3.
2. **Load:** Raw data loaded from S3 into Snowflake staging tables.
3. **Silver (cleaned):** dbt staging models — clean types, dedupe, standardize.
4. **Gold (modeled):** dbt mart models — a proper star schema: `fact_orders` + 
   `dim_customers`, `dim_products`, `dim_sellers`, `dim_date`, `dim_geography`.
5. **Quality:** dbt tests (uniqueness, not-null, referential integrity) + 
   auto-generated dbt docs/lineage.
6. **Orchestration:** Apache Airflow (run via Docker locally) — a DAG chains 
   extract → load → transform → test, on a schedule.
7. **CI/CD:** GitHub Actions — runs dbt tests automatically on every push/PR.
8. *(Stretch goal, not yet started)*: enrich with a live API pull (e.g. daily 
   BRL/USD exchange rate) to show recurring ingestion, not just a one-time load.

## Tech stack
- **Language:** Python
- **Version control:** Git + GitHub (repo: `ecommerce-data-pipeline`, cloned 
  locally as `olist-dataset-pipeline`)
- **Editor:** VS Code
- **Raw storage:** AWS S3 (free tier)
- **Warehouse:** Snowflake (free trial, Standard edition, AWS-hosted, US East region)
- **Transformation:** dbt Core + dbt-snowflake adapter
- **Orchestration:** Apache Airflow via Docker Compose (NOT installed bare-metal 
  in the venv — deliberately excluded from requirements.txt because Airflow is 
  painful to install directly; will run via official Docker image instead)
- **CI/CD:** GitHub Actions
- **Data source:** Kaggle API (`kaggle` Python package)

## Environment setup status — ALL COMPLETE
- ✅ GitHub repo created and cloned locally to `E:\Projects\olist-dataset-pipeline`
- ✅ Python virtual environment created and activated (`venv`)
- ✅ Folder structure created: `dags/`, `extract/`, `docker/`, `dbt_project/`
- ✅ `requirements.txt` created and installed successfully:
boto3==1.34.0
kaggle==1.6.6
python-dotenv==1.0.1
pandas==2.2.0
snowflake-connector-python==3.7.0
dbt-snowflake==1.7.1

  (Verified via `python -c "import boto3, pandas, snowflake.connector; print('All good')"` 
  — succeeded, only a harmless pandas/pyarrow deprecation warning.)
- ✅ AWS account created, billing alarm set up
- ✅ AWS IAM user created (`ecommerce-pipeline-user`) with `AmazonS3FullAccess` 
  policy, Access Key ID + Secret Access Key generated
- ✅ S3 bucket created
- ✅ Snowflake account created (free trial, Standard edition, AWS provider)
- ✅ Docker Desktop installed and running
- ✅ `.env` file created at repo root with real credentials filled in (AWS keys, 
  region, bucket name, Snowflake account/user/password/warehouse/database/schema). 
  `.env` is in `.gitignore` — confirmed not tracked by Git.
- ✅ `.env.example` created as a template (placeholder values only, safe to commit)
- ✅ Kaggle API credentials working: `kaggle.json` placed at 
  `C:\Users\Monank\.kaggle\kaggle.json`, verified via 
  `kaggle datasets list -s olist` — successfully listed 
  `olistbr/brazilian-ecommerce` (43MB dataset) among results

## .env structure (values are real in the actual file, this is the template)

AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=...
S3_BUCKET_NAME=...

SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=OLIST_DB
SNOWFLAKE_SCHEMA=RAW


## What's NOT done yet (next steps, in order)
1. **Extract script** (`extract/` folder) — Python script to download the Olist 
   dataset via Kaggle API and upload each CSV to the S3 bucket. This is the very 
   next task.
2. Load script/process — get raw CSVs from S3 into Snowflake staging tables.
3. dbt project setup inside `dbt_project/` — staging models (Silver layer).
4. dbt mart models — the star schema (Gold layer): `fact_orders`, `dim_customers`, 
   `dim_products`, `dim_sellers`, `dim_date`, `dim_geography`.
5. dbt tests (uniqueness, not-null, referential integrity) + dbt docs generation.
6. Airflow DAG (in `dags/`) + Docker Compose setup (in `docker/`) to orchestrate 
   the whole pipeline.
7. GitHub Actions workflow for CI (run dbt tests on push/PR).
8. Stretch: live exchange-rate API enrichment via the Airflow DAG.
9. Eventually: this project's output (the Snowflake warehouse) becomes the input 
   for Flagship Project 2 (statistics/ML/dashboard project) — not yet designed 
   in detail, but planned to query this same warehouse.

## Working style notes
- I'm learning as I go — prior conversation involved step-by-step guidance through 
  account setup, terminal commands, and troubleshooting (e.g. PowerShell vs CMD 
  syntax differences, Kaggle token download issues).
- I'm on Windows, using CMD (not PowerShell) in the VS Code integrated terminal.
- I want to understand *why* each tool/step is used, not just copy-paste commands 
  blindly — explanations of purpose have been appreciated throughout.