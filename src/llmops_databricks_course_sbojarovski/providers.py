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
