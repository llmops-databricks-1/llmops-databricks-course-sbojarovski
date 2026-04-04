"""
This module contains common "providers"  -- recipes for creating services
"""

from arxiv import Client  # type: ignore[import-untyped]
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from openai import OpenAI
from pyspark.sql import SparkSession


def provide_spark_session() -> SparkSession:
    return DatabricksSession.builder.getOrCreate()


def provide_workspace_client() -> WorkspaceClient:
    return WorkspaceClient()


def provide_mosaic_ai_client(
    wc: WorkspaceClient,
) -> OpenAI:
    return OpenAI(
        api_key=wc.tokens.create(lifetime_seconds=60 * 60).token_value,
        base_url=f"{wc.config.host}/serving-endpoints",
    )


def provide_arxiv_client() -> Client:
    return Client()


def provide_databricks_dbutils():
    """Provides a dbutils instance in an encapsulated manner.

    Imports dbutils at runtime to avoid credential issues when importing
    at module level. This allows notebooks to be run both locally and
    on Databricks.
    """
    from databricks.sdk.runtime import dbutils

    return dbutils
