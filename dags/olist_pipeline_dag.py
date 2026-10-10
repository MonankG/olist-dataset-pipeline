from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="olist_pipeline",
    description="Extract Olist data to S3, load to Snowflake, transform with dbt, and test",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="python /opt/airflow/extract/extract_to_s3.py",
    )

    load = BashOperator(
        task_id="load",
        bash_command="python /opt/airflow/load/load_to_snowflake.py",
    )

    fetch_exchange_rate = BashOperator(
        task_id="fetch_exchange_rate",
        bash_command="python /opt/airflow/extract/fetch_exchange_rate.py",
    )

    load_exchange_rate = BashOperator(
        task_id="load_exchange_rate",
        bash_command="python /opt/airflow/load/load_exchange_rate.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run --project-dir /opt/airflow/dbt_project --profiles-dir /opt/airflow/dbt_project",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="dbt test --project-dir /opt/airflow/dbt_project --profiles-dir /opt/airflow/dbt_project",
    )

    extract >> load
    fetch_exchange_rate >> load_exchange_rate
    [load, load_exchange_rate] >> dbt_run >> dbt_test
