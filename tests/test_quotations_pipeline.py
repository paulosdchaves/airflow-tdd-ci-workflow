import subprocess

import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


def execute_dag(dag_id, execution_date):
    """Execute a DAG in a specific date this process wait for DAG run or fail to continue"""
    subprocess.run(["airflow", "dags", "backfill", "-s", execution_date, dag_id])


# test_quotations_pipeline.py
class TestQuotationsPipeline:
    def test_validate_quotations_pipeline(self):

        legacy_hook = PostgresHook("legacy")
        legacy_hook.run(
            """
        CREATE TABLE IF NOT EXISTS products (
            planselected_id          INTEGER,
            planselected_name        TEXT,
            reportedcapitalvalue     INTEGER,
            insurancepremium_annual  INTEGER
        );
        """
        )

        legacy_conn = legacy_hook.get_sqlalchemy_engine()
        sample_data = pd.read_csv("./data/products.csv")
        sample_data.to_sql(
            name="products",  # name of sql table
            con=legacy_conn,  # SQLalchemy connection
            if_exists="replace",  # refresh data if run again
            index=False,  # don't want the pandas index inside db table
        )

        analytics_hook = PostgresHook("analytics")
        analytics_hook.run(
            """
        CREATE TABLE IF NOT EXISTS products (
            planselected_id          INTEGER,
            planselected_name        TEXT,
            reportedcapitalvalue     INTEGER,
            insurancepremium_annual  INTEGER
        );
        """
        )

        date = "2021-09-01"
        execute_dag("quotations_pipeline", date)

        analytics_product_size = analytics_hook.get_records("select * from products")
        assert len(analytics_product_size) == 2
