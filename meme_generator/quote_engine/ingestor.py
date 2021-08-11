"""Module to parse files into QuoteModels."""

from typing import List
from abc import ABC, abstractmethod

from meme_generator.quote_engine import QuoteModel
from meme_generator.errors import (NotImplementedError,
                                   InputNotSupportedError)
from meme_generator.quote_engine.txt_ingestor import TextIngestor
from meme_generator.quote_engine.pdf_ingestor import PdfIngestor
from meme_generator.quote_engine.csv_ingestor import CsvIngestor
from meme_generator.quote_engine.docx_ingestor import DocxIngestor
from meme_generator.quote_engine.interface import IngestorInterface


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
