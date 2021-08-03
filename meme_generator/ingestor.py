"""Module to parse files into QuoteModels."""

from typing import List
from abc import ABC, abstractmethod
import pandas

from meme_generator.quote_engine import QuoteModel
from meme_generator.errors import (NotImplementedError,
                                   InputNotSupportedError)
from meme_generator.fileio import (convert_pdf_to_txt,
                                   system_remove_file,
                                   read_txt,
                                   read_csv, read_docx)


class IngestorInterface(ABC):
    """Abstract class to be the interface for ingestors."""

    extension = ""

    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        """Check whether given file can be ingested."""
        raise NotImplementedError

    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse given file into QuoteModel objects."""
        raise NotImplementedError


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


class CsvIngestor(IngestorInterface):
    """Class to ingest QuoteModels given a CSV file."""

    extension = ".csv"

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check whether given file can be ingested."""
        if path.lower().endswith(cls.extension):
            return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse given file into QuoteModel objects using pandas library."""
        contents = pandas.read_csv(path)
        models = [QuoteModel(d["body"], d["author"])
                  for i, d in contents.iterrows()]
        return models


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
