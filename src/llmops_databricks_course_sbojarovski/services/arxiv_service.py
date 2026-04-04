import time
from dataclasses import dataclass
from datetime import datetime

from arxiv import Client, Search  # type: ignore[import-untyped]


@dataclass
class PaperRecord:
    paper_id: str
    title: str
    authors: list[str]
    summary: str
    pdf_url: str
    published_datetime: datetime


class ArxivService:
    """
    Wrapper around the Arxiv API which provides domain specific
    methods for ingesting PDF articles
    """

    def __init__(self, arxiv_client: Client):
        self.arxiv_client = arxiv_client
        self.TIMESTAMP_FORMAT = "%Y%m%d%H%M"

    def _format_timestamp(self, dt: datetime) -> str:
        """Format datetime to arXiv API timestamp format."""
        return dt.strftime(self.TIMESTAMP_FORMAT)

    def search_papers(
        self,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[PaperRecord]:

        search = Search(
            query=f"cat:cs.AI AND submittedDate:[{self._format_timestamp(start_datetime)} TO {self._format_timestamp(end_datetime)}]",
        )

        records = []
        for paper in self.arxiv_client.results(search):
            records.append(
                PaperRecord(
                    paper_id=paper.get_short_id(),
                    title=paper.title,
                    authors=[author.name for author in paper.authors],
                    summary=paper.summary,
                    pdf_url=paper.pdf_url,
                    published_datetime=paper.published,
                )
            )
            time.sleep(3)

        return records
