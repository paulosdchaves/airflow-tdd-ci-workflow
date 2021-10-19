import subprocess

import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pandas._testing import assert_frame_equal


def insert_initial_data(tablename, hook):
    """This script will populate database with initial data to run job"""
    conn_engine = hook.get_sqlalchemy_engine()
    sample_data = pd.read_csv(f"/opt/airflow/data/{tablename}.csv")
    sample_data.to_sql(
        name=tablename, con=conn_engine, if_exists="replace", index=False
    )


def create_table(tablename, hook):
    sql_query = open(f"/opt/airflow/sql/init/create_{tablename}.sql").read()
    hook.run(sql_query.format(tablename=tablename))


def output_df(filename):
    return pd.read_csv(f"/opt/airflow/tests/fixtures/{filename}.csv")


def execute_dag(dag_id, execution_date):
    """Execute a DAG in a specific date this process wait for DAG run or fail to continue"""
    subprocess.run(["airflow", "dags", "backfill", "-s", execution_date, dag_id])


# test_quotations_pipeline.py
class TestQuotationsPipeline:
    def test_validate_quotations_pipeline(self):

        legacy_hook = PostgresHook("legacy")

        create_table("products", legacy_hook)
        insert_initial_data("products", legacy_hook)

        analytics_hook = PostgresHook("analytics")
        create_table("products", analytics_hook)

        date = "2021-09-01"
        execute_dag("quotations_pipeline", date)

        analytics_product_size = analytics_hook.get_records("select * from products")
        assert len(analytics_product_size) == 2

        expected_product_data = output_df("products")

        analytics_product_data = analytics_hook.get_pandas_df("select * from products")
        assert_frame_equal(analytics_product_data, expected_product_data)
