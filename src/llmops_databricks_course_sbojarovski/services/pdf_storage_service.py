from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import max

from llmops_databricks_course_sbojarovski.config import settings
from llmops_databricks_course_sbojarovski.services.arxiv_service import PaperRecord


class PDFStorageService:
    """
    This service is responsible for materializing
    the retrieved PDF data from the Arxiv API and provides
    a checkpoint to the latest ingested batch in order to enable
    incremental ingestion.
    """

    def __init__(
        self,
        spark: SparkSession,
    ):
        self.spark = spark

        self.EARLIEST_PUBLISH_DATETIME = datetime.fromisoformat("2025-01-01")

    @property
    def checkpoint(
        self,
    ) -> datetime:
        latest_published_datetime = (
            self.spark.read.table(settings.PDF_STORED_METADATA_TABLE_NAME)
            .agg(max("published_datetime"))
            .collect()[0][0]
        )

        if latest_published_datetime is None:
            return self.EARLIEST_PUBLISH_DATETIME

        return datetime.fromisoformat(latest_published_datetime)

    def store(
        self,
        papers_metadata: list[PaperRecord],
    ) -> None:
        pass
