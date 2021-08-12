"""Module to parse files into QuoteModels."""

from typing import List
from abc import ABC, abstractmethod

from .quote_engine import QuoteModel
from .txt_ingestor import TextIngestor
from .pdf_ingestor import PdfIngestor
from .csv_ingestor import CsvIngestor
from .docx_ingestor import DocxIngestor
from .interface import IngestorInterface
from ..errors import InputNotSupportedError


class Ingestor(IngestorInterface):
    """Class to ingest QuoteModels given different kind of files.

    Supports PDF, CSV, TXT and DOCX formats.
    """

    ingestors = [PdfIngestor, CsvIngestor, TextIngestor, DocxIngestor]

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check whether given file can be ingested."""
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse given file into QuoteModel objects."""
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        extensions = [i.extension for i in cls.ingestors]
        raise InputNotSupportedError(
            f"Can't parse path '{path}'. Supported extensions are: "
            f"{extensions}")
