from datetime import datetime

from arxiv import Client, Result, Search  # type: ignore[import-untyped]


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
    ) -> list[Result]:

        search = Search(
            query=f"cat:cs.AI AND submittedDate:[{self._format_timestamp(start_datetime)} TO {self._format_timestamp(end_datetime)}]",
        )

        return list(self.arxiv_client.results(search))
