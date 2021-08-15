"""Module to parse files into QuoteModels."""

from typing import List

from .quote_engine import QuoteModel
from .interface import IngestorInterface
from .txt_ingestor import TextIngestor
from meme_generator.fileio import (convert_pdf_to_txt,
                                   system_remove_file)


class PdfIngestor(IngestorInterface):
    """Class to ingest QuoteModels given a PDF file using subprocess."""

    extension = ".pdf"

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check whether given file can be ingested."""
        if path.lower().endswith(cls.extension):
            return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse given file into QuoteModel objects."""
        tmp_file = convert_pdf_to_txt(path)
        parsed = TextIngestor.parse(tmp_file)
        system_remove_file(tmp_file)
        return parsed
