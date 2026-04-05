import logging
from datetime import datetime

from arxiv import Result

from llmops_databricks_course_sbojarovski.services.arxiv_service import (
    ArxivService,
)
from llmops_databricks_course_sbojarovski.services.pdf_storage_service import (
    PDFStorageService,
)
from llmops_databricks_course_sbojarovski.utils.date_utils import iterate_day_intervals

logger = logging.getLogger(__name__)


class DataIngestionService:
    def __init__(
        self,
        arxiv_service: ArxivService,
        pdf_storage_service: PDFStorageService,
    ):
        self.arxiv_service = arxiv_service
        self.pdf_storage_service = pdf_storage_service

    def ingest_for_interval(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> None:
        logger.info(f"Ingesting data for interval: {start_datetime} to {end_datetime}")
        papers: list[Result] = self.arxiv_service.search_papers(
            start_datetime, end_datetime
        )
        # TODO: if the storage of paper records fails mid-batch, on the next
        #      run we will miss the papers not stored from the batch and continue
        #      from the next date interval
        self.pdf_storage_service.store(papers)

    def ingest(
        self,
    ) -> None:
        start_datetime: datetime = self.pdf_storage_service.checkpoint
        end_datetime: datetime = datetime.now()

        logger.info(f"Ingesting data from {start_datetime} to {end_datetime}")
        for start_interval, end_interval in iterate_day_intervals(
            start_datetime, end_datetime
        ):
            self.ingest_for_interval(start_interval, end_interval)
        logger.info(f"Finished ingesting data for {start_datetime} to {end_datetime}")
