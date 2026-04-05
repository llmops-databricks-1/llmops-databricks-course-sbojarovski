"""
This module contains common "providers"  -- recipes for creating services
"""

from typing import TYPE_CHECKING

from arxiv import Client  # type: ignore[import-untyped]
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from databricks.sdk.runtime import DBUtils
from openai import OpenAI
from pyspark.sql import SparkSession

if TYPE_CHECKING:
    from llmops_databricks_course_sbojarovski.services.arxiv_service import (
        ArxivService,
    )
    from llmops_databricks_course_sbojarovski.services.data_ingestion_service import (
        DataIngestionService,
    )
    from llmops_databricks_course_sbojarovski.services.pdf_storage_service import (
        PDFStorageService,
    )


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


def provide_databricks_dbutils() -> DBUtils:
    """Provides a dbutils instance in an encapsulated manner.

    Imports dbutils at runtime to avoid credential issues when importing
    at module level. This allows notebooks to be run both locally and
    on Databricks.
    """
    from databricks.sdk.runtime import dbutils

    return dbutils


def provide_arxiv_service() -> "ArxivService":
    from llmops_databricks_course_sbojarovski.services.arxiv_service import ArxivService

    return ArxivService(arxiv_client=provide_arxiv_client())


def provide_pdf_storage_service() -> "PDFStorageService":
    from llmops_databricks_course_sbojarovski.services.pdf_storage_service import (
        PDFStorageService,
    )

    return PDFStorageService(
        spark=provide_spark_session(),
    )


def provide_data_ingestion_service() -> "DataIngestionService":
    from llmops_databricks_course_sbojarovski.services.data_ingestion_service import (
        DataIngestionService,
    )

    return DataIngestionService(
        arxiv_service=provide_arxiv_service(),
        pdf_storage_service=provide_pdf_storage_service(),
    )
