"""Module to parse files into QuoteModels."""

from typing import List
from abc import ABC, abstractmethod

from .quote_engine import QuoteModel
from ..errors import NotImplementedError


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
