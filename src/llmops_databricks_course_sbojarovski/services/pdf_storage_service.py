import time
from datetime import datetime

from arxiv import Result
from pyspark.sql import SparkSession
from pyspark.sql.functions import max
from pyspark.sql.types import (
    ArrayType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

from llmops_databricks_course_sbojarovski.config import settings


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
            self.spark.read.table(settings.PDF_STORAGE_METADATA_TABLE_FULL_NAME)
            .agg(max("published_datetime"))
            .collect()[0][0]
        )

        if latest_published_datetime is None:
            return self.EARLIEST_PUBLISH_DATETIME

        return datetime.fromisoformat(latest_published_datetime)

    def _store_papers_metadata(self, papers: list[Result]) -> None:

        # Convert PaperRecords to list of dicts
        paper_dicts = [
            {
                "paper_id": record.get_short_id(),
                "title": record.title,
                "authors": record.authors,
                "summary": record.summary,
                "published_datetime": record.published,
                "processed_datetime": None,  # Will be set after PDF is processed
                "volume_path": None,  # Will be set after PDF download
            }
            for record in papers
        ]

        # Create DataFrame with matching schema
        schema = StructType(
            [
                StructField("paper_id", StringType(), False),
                StructField("title", StringType(), True),
                StructField("authors", ArrayType(StringType()), True),
                StructField("summary", StringType(), True),
                StructField("published_datetime", TimestampType(), True),
                StructField("processed_datetime", TimestampType(), True),
                StructField("volume_path", StringType(), True),
            ]
        )

        df = self.spark.createDataFrame(paper_dicts, schema=schema)
        df.createOrReplaceTempView("temp_papers")  # Replaces previous, no cleanup needed

        self.spark.sql(f"""
              MERGE INTO {settings.PDF_STORAGE_METADATA_TABLE_FULL_NAME} t
              USING temp_papers s
              ON t.paper_id = s.paper_id
              WHEN NOT MATCHED THEN INSERT (
                  paper_id, title, authors, summary, published_datetime, processed_datetime, volume_path
              ) VALUES (
                  s.paper_id, s.title, s.authors, s.summary, s.published_datetime, s.processed_datetime, s.volume_path
              )
              ;
        """)

    def _store_papers_pdf(self, papers: list[Result]) -> None:
        pdf_paths = []
        for paper in papers:
            paper.download_pdf(
                dirpath=settings.PDF_STORAGE_VOLUME_FULL_PATH,
                filename=f"{paper.get_short_id()}.pdf",
            )
            pdf_paths.append(
                {
                    "paper_id": paper.get_short_id(),
                    "volume_path": f"{settings.PDF_STORAGE_VOLUME_FULL_PATH}/{paper.get_short_id()}.pdf",
                }
            )
            time.sleep(3)

        schema = StructType([StructField("volume_path", StringType(), True)])
        df = self.spark.createDataFrame(pdf_paths, schema=schema)
        df.createOrReplaceTempView("temp_paths")  # Replaces previous, no cleanup needed

        self.spark.sql(f"""
            MERGE INTO {settings.PDF_STORAGE_METADATA_TABLE_FULL_NAME} t
            USING temp_paths s
            ON t.paper_id = s.paper_id
            WHEN MATCHED THEN UPDATE SET
                t.volume_path = s.volume_path
            ;
        """)

    def store(
        self,
        papers_metadata: list[Result],
    ) -> None:
        self._store_papers_metadata(papers_metadata)
        self._store_papers_pdf(papers_metadata)
