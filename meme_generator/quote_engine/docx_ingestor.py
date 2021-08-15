"""Module to parse files into QuoteModels."""

from typing import List

from .quote_engine import QuoteModel
from .interface import IngestorInterface
from meme_generator.fileio import read_docx


class DocxIngestor(IngestorInterface):
    """Class to ingest QuoteModels given a DOCX file."""

    extension = ".docx"

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check whether given file can be ingested."""
        if path.lower().endswith(cls.extension):
            return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse given file into QuoteModel objects."""
        contents = read_docx(path)
        models = [QuoteModel(*line.split(" - ")) for line in contents]
        return models
