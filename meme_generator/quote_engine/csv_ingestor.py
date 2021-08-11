"""Module to parse files into QuoteModels."""

from typing import List
import pandas

from meme_generator.quote_engine import QuoteModel
from meme_generator.quote_engine.interface import IngestorInterface


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
