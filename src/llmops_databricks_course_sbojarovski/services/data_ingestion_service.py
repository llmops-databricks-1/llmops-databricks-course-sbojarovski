from datetime import datetime

from llmops_databricks_course_sbojarovski.services.arxiv_service import (
    ArxivService,
    PaperRecord,
)
from llmops_databricks_course_sbojarovski.services.pdf_storage_service import (
    PDFStorageService,
)
from llmops_databricks_course_sbojarovski.utils.date_utils import iterate_day_intervals


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
        papers: list[PaperRecord] = self.arxiv_service.search_papers(
            start_datetime, end_datetime
        )
        self.pdf_storage_service.store(papers)

    def ingest(
        self,
    ) -> None:
        start_datetime: datetime = self.pdf_storage_service.checkpoint
        end_datetime: datetime = datetime.now()

        for start_interval, end_interval in iterate_day_intervals(
            start_datetime, end_datetime
        ):
            self.ingest_for_interval(start_interval, end_interval)
