"""Module to parse files into QuoteModels."""

from typing import List

from .quote_engine import QuoteModel
from .interface import IngestorInterface
from ..fileio import read_txt


class TextIngestor(IngestorInterface):
    """Class to ingest QuoteModels given a TXT file."""

    extension = ".txt"

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check whether given file can be ingested."""
        if path.lower().endswith(cls.extension):
            return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse given file into QuoteModel objects."""
        contents = read_txt(path)
        models = [QuoteModel(*line.split(" - ")) for line in contents]
        return models
