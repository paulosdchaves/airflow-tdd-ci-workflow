from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago


def transfer_data(**kwargs):
    """Get records from legacy and transfer to analytics database"""
    dest_table = kwargs.get("dest_table")
    sql = kwargs.get("sql")
    params = kwargs.get("params")

    legacy_hook = PostgresHook(postgres_conn_id="legacy")
    analytics_hook = PostgresHook(postgres_conn_id="analytics")
    data_extracted = legacy_hook.get_records(sql=sql, parameters=params)
    analytics_hook.insert_rows(dest_table, data_extracted, commit_every=1000)


with DAG(
    dag_id="quotations_pipeline",
    default_args={"owner": "airflow"},
    schedule_interval=None,
    start_date=days_ago(2),
    template_searchpath="/opt/airflow/sql/sales/",
    tags=["etl", "analytics", "insurance", "quotation", "dag"],
) as dag:

    load_full_products_data = PythonOperator(
        task_id="load_full_products",
        python_callable=transfer_data,
        op_kwargs={
            "dest_table": "products",
            "sql": "select * from products",
        },
    )
