---
name: memory
description: Running record of what has been done on the olist-dataset-pipeline project so far. Read this first when picking work back up to know current state and what's next.
---

# Project Memory

This file is the single source of truth for project progress. It is updated by the
`update-memory` skill after each completed task, not edited freely otherwise.

## Background
Student graduating Spring 2027, targeting Data Engineer / Data Analyst / Data Scientist /
Software Engineer / Automation roles. This repo is "Flagship Project 1," built to
demonstrate Data Engineering skills (Python, SQL, ETL, dbt, Airflow, Git, AWS, Snowflake,
data governance). Its output warehouse will later feed "Flagship Project 2"
(stats/ML/dashboard, not yet designed).

## What the project is
End-to-end pipeline on the public Olist Brazilian E-Commerce dataset (Kaggle:
`olistbr/brazilian-ecommerce`, ~100K orders, 9 relational CSVs). Medallion architecture:
Kaggle -> S3 (Bronze) -> Snowflake staging -> dbt staging models (Silver) -> dbt star
schema marts (Gold: fact_orders, dim_customers, dim_products, dim_sellers, dim_date,
dim_geography) -> dbt tests/docs -> Airflow (Docker) orchestration -> GitHub Actions CI.
Stretch goal: daily BRL/USD exchange-rate API enrichment.

Tech stack: Python, Git/GitHub, VS Code, AWS S3 (free tier), Snowflake (free trial),
dbt Core + dbt-snowflake, Apache Airflow via Docker Compose (not installed bare-metal),
GitHub Actions, Kaggle API.

## Environment setup status
- GitHub repo cloned to `E:\Projects\olist-dataset-pipeline`
- Python venv created, `requirements.txt` installed and import-verified
- Folders created: `dags/`, `extract/`, `docker/`, `dbt_project/`
- AWS account + billing alarm + IAM user `ecommerce-pipeline-user` (AmazonS3FullAccess) + access keys
- S3 bucket created
- Snowflake free-trial account created (Standard edition, AWS-hosted, US East).
  MFA is enforced on user MONANKKK, so scripts authenticate via RSA key-pair
  (`keys/rsa_key.p8`, gitignored) rather than `SNOWFLAKE_PASSWORD` — see
  `load/load_to_snowflake.py`.
- Docker Desktop installed and running
- `.env` populated with real credentials (gitignored, confirmed untracked); `.env.example` committed
- Kaggle API credentials working (`kaggle.json` at `C:\Users\Monank\.kaggle\kaggle.json`)

## Progress log
(Newest entries at the top. Each entry: date, what was done, files touched, what's next.)

- **2026-10-06** — Generated 2 interview-prep notes under `notes/Data
  Engineering/`: Airflow DAGs & Orchestration (incl. the paused-DAG gotcha)
  and Docker & Docker Compose for Data Pipelines. Updated
  `notes/Knowledge-Map.md`. 11 notes total now.
- **2026-10-06** — Built and fully verified the Airflow + Docker orchestration
  layer: `docker/Dockerfile` (extends `apache/airflow:2.8.1-python3.10`,
  installs root `requirements.txt` into the image), `docker/docker-compose.yml`
  (Postgres metadata DB + airflow-init + airflow-webserver + airflow-scheduler,
  LocalExecutor, mounts `dags/`, `extract/`, `load/`, `dbt_project/`, and two
  new gitignored credential folders `keys/` (RSA private key) and `kaggle/`
  (kaggle.json, copied in by the user — Claude is blocked from copying
  credential files directly, a safety classifier denial, so this step needs
  the user to run the `cp`/`copy` themselves)), and `dags/olist_pipeline_dag.py`
  (`extract >> load >> dbt_run >> dbt_test`, daily schedule).
  Built the image, ran `airflow-init`, started webserver+scheduler, confirmed
  the DAG parsed with 0 import errors.
  Hit a real gotcha: triggered DAG runs stayed stuck in `queued` forever even
  though the scheduler process was alive and heartbeating — root cause was
  that **new DAGs are paused by default** in Airflow, and a paused DAG's runs
  never get scheduled even when manually triggered. Fixed with
  `airflow dags unpause olist_pipeline`; the two stale pre-unpause runs
  auto-failed (expected cleanup), and a fresh triggered run succeeded end to
  end: extract (verified real Kaggle download + S3 upload in the task log,
  not a stub) -> load -> dbt_run -> dbt_test (33/33 passed), confirmed via
  task logs. Tore the stack down afterward with `docker compose down`
  (`.env` loaded via `--env-file .env`, must run `docker compose` with
  `-f docker/docker-compose.yml --env-file .env` from the project root).
  Orchestration step is now done — the full pipeline runs unattended via
  Airflow.
- **2026-10-05** — Generated interview-prep note "dbt Tests & Data Governance"
  under `notes/Data Engineering/` (generic tests, relationships/referential
  integrity, docs/lineage). Updated `notes/Knowledge-Map.md`.
- **2026-10-05** — Added dbt data-quality tests and generated docs/lineage:
  `dbt_project/models/staging/_staging.yml` (not_null/unique on staging
  natural keys) and `dbt_project/models/marts/_marts.yml` (not_null/unique on
  dim primary keys, plus `relationships` tests on `fact_orders.customer_id
  -> dim_customers`, `.product_id -> dim_products`, `.seller_id ->
  dim_sellers` for referential integrity). `dbt test`: 33/33 passed.
  `dbt docs generate` ran successfully (catalog.json/manifest.json in
  `dbt_project/target/`, gitignored along with `dbt_packages/` and `logs/`).
  dbt layer (staging + marts + tests + docs) is now fully done.
- **2026-10-05** — Generated interview-prep note "Star Schema & Fact Table
  Grain" under `notes/Data Engineering/` (fact/dim design, grain selection,
  and the fan-out/double-counting trap from fact_orders). Updated
  `notes/Knowledge-Map.md`.
- **2026-10-05** — Built and verified the dbt mart models (Gold layer / star
  schema) in `dbt_project/models/marts/`: `dim_customers`, `dim_products`
  (joined to category translation), `dim_sellers`, `dim_geography`
  (geolocation collapsed to one row per zip, avg lat/lng, MIN() for a
  deterministic city/state), `dim_date` (1500-day calendar spine via
  Snowflake's GENERATOR, no dbt package dependency), and `fact_orders`.
  Key design decision: `fact_orders` grain is one row per **order item**
  (not per order), since that's what lets it join to `dim_products` and
  `dim_sellers` (an order can span multiple products/sellers). Order-level
  attributes (status, dates, review_score) are duplicated across an order's
  items and must not be summed across items of the same order; only
  `price`/`freight_value` are treated as additive measures. All materialized
  as tables (`+materialized: table` for `marts` in `dbt_project.yml`, vs.
  `view` for staging). `dbt run` succeeded: 15/15 models (9 staging views + 6
  marts). Spot-checked `fact_orders` via `dbt show`. Gold layer is now done —
  the full star schema exists in `OLIST_DB.ANALYTICS`.
- **2026-09-29** — Generated interview-prep note "dbt Sources & Staging Models"
  under `notes/Data Engineering/` (covers sources.yml, the staging pattern,
  view materialization, and the Snowflake identifier-casing bug). Updated
  `notes/Knowledge-Map.md`.
- **2026-09-29** — Built and verified dbt staging models (Silver layer):
  `dbt_project/` now has `dbt_project.yml`, `profiles.yml` (Snowflake target
  `dev`, key-pair auth via `SNOWFLAKE_PRIVATE_KEY_PATH`, target schema
  `ANALYTICS` set via new `SNOWFLAKE_DBT_SCHEMA` env var), a source definition
  (`models/staging/_sources.yml`, pointing at `OLIST_DB.RAW`), and 9 staging
  models (`stg_customers`, `stg_geolocation`, `stg_order_items`,
  `stg_order_payments`, `stg_order_reviews`, `stg_orders`, `stg_products`,
  `stg_sellers`, `stg_product_category_translation`) that cast the raw
  VARCHAR columns to proper types (int/float/timestamp_ntz) as views.
  Hit and fixed a real issue: the load script's `CREATE TABLE` had quoted
  lowercase column names (`"customer_id"`), which Snowflake then treated as
  case-sensitive identifiers — dbt's unquoted `customer_id` normalizes to
  uppercase `CUSTOMER_ID` and didn't match, causing `invalid identifier`
  errors on every model. Fixed by removing the quotes in
  `load/load_to_snowflake.py` (now `{col} VARCHAR` unquoted, so Snowflake
  auto-uppercases consistently) and re-running the load. `dbt run` then
  succeeded: 9/9 models built (`dbt debug` also passes). `.env`/`.env.example`
  gained `SNOWFLAKE_PRIVATE_KEY_PATH` and `SNOWFLAKE_DBT_SCHEMA`. Invocation:
  `set -a && source .env && set +a && DBT_PROFILES_DIR=dbt_project dbt run
  --project-dir dbt_project` (dbt doesn't auto-load `.env`, must be sourced
  into the shell first).
- **2026-09-29** — Generated 2 more interview-prep notes under `notes/Data
  Engineering/`: Snowflake Staging & COPY INTO, and Snowflake Key-Pair
  Authentication (grounded in the MFA issue hit and fixed during the load
  step). Updated `notes/Knowledge-Map.md`.
- **2026-09-29** — Built and verified the load script: `load/load_to_snowflake.py`
  loads all 9 raw CSVs from S3 directly into Snowflake (OLIST_DB.RAW schema) via
  an external stage + COPY INTO, one VARCHAR-only table per CSV (typing happens
  later in dbt). Hit two real issues along the way:
  1. Snowflake account has MFA enforced, so password auth failed for the script
     (`MFA authentication is required, but none of your current MFA methods are
     supported for programmatic authentication`). Fixed by switching to
     **key-pair authentication**: generated an RSA key pair (`keys/rsa_key.p8`
     private, `keys/rsa_key.pub` public — `keys/` added to `.gitignore`,
     private key never committed), registered the public key on user
     `MONANKKK` via `ALTER USER ... SET RSA_PUBLIC_KEY=...`, and updated the
     script to authenticate with the private key instead of
     `SNOWFLAKE_PASSWORD`.
  2. `CREATE FILE FORMAT`/`CREATE STAGE` failed with "no current database" even
     though database/schema were passed to `connect()` — fixed by having the
     script explicitly run `CREATE DATABASE/SCHEMA IF NOT EXISTS` and
     `USE WAREHOUSE/DATABASE/SCHEMA` right after connecting.
  Verified: all 9 tables loaded successfully (row counts match source CSVs,
  e.g. CUSTOMERS 99441, GEOLOCATION 1000163, ORDERS 99441). Load step (S3 ->
  Snowflake staging) is now done.
- **2026-09-29** — Generated the first interview-prep notes under `notes/Data
  Engineering/`: AWS S3, IAM & Least-Privilege Access, and Kaggle API, each as a
  `Topic-Name-Notes.docx` following the AGENTS.md note structure, grounded in the
  actual extract-script worked example (IAM AccessDenied fix included). Updated
  `notes/Knowledge-Map.md` with all three. User asked that notes be generated
  automatically after crucial project milestones going forward, not just on request.
- **2026-09-29** — Built and verified the extract script: `extract/extract_to_s3.py`
  downloads the Olist dataset via the Kaggle API and uploads all 9 raw CSVs
  untouched to `s3://monank-olist-dataset/raw/olist/`. Hit and fixed an IAM
  permissions gap along the way: IAM user `olist-dataset-pipeline` had valid
  credentials but no S3 policy attached; added an inline policy (`olist-s3-access`)
  scoped to just this bucket (PutObject/GetObject/ListBucket). Also added
  `venv/`, `extract/data/`, and `olist-dataset-pipeline_credentials.csv` to
  `.gitignore`. Bronze layer (extract step) is now done and verified working.
- **2026-09-29** — Set up the interview-notes system: created `notes/` at project
  root with `notes/Knowledge-Map.md` as the index, plus the `knowledge-base` skill
  (points to the note system/format) and `update-knowledge-base` skill (generates
  `Topic-Name-Notes.docx` files under `notes/<Area>/<Topic>/` following the note
  structure/formatting rules added to AGENTS.md). Files: `notes/Knowledge-Map.md`,
  `.agents/skills/knowledge-base/SKILL.md`, `.agents/skills/update-knowledge-base/SKILL.md`.
  No topic notes written yet — will be generated as concepts come up. No pipeline
  code written yet either.
- **2026-09-28** — Recovered project context from a prior chat session (pasted into
  `.agents/skills/project-context/SKILL.md`) after the original claude.ai share link
  wasn't accessible to this session. Created this `memory` skill and the
  `update-memory` skill per AGENTS.md conventions. No pipeline code written yet.

## What's NOT done yet (next steps, in order)
1. GitHub Actions CI workflow (dbt tests on push/PR). This is the next task.
2. Stretch: live exchange-rate API enrichment via the Airflow DAG.
3. Eventually: warehouse becomes input for Flagship Project 2.
