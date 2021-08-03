"""Tests of ingestor module."""

from meme_generator.quote_engine import QuoteModel
from meme_generator.ingestor import Ingestor
from tests.helpers.helpers import (quotes_pdf, quotes_txt,
                                   quotes_csv, quotes_docx)


def test_can_ingest_given_txt_when_parsed_then_quotes(quotes_txt):
    quotes = Ingestor.parse(str(quotes_txt))
    assert quotes
    assert all([type(quote) == QuoteModel for quote in quotes])


def test_can_ingest_given_pdf_when_parsed_then_quotes(quotes_pdf):
    quotes = Ingestor.parse(str(quotes_pdf))
    assert quotes
    assert all([type(quote) == QuoteModel for quote in quotes])


def test_can_ingest_given_csv_when_parsed_then_quotes(quotes_csv):
    quotes = Ingestor.parse(str(quotes_csv))
    assert quotes
    assert all([type(quote) == QuoteModel for quote in quotes])


def test_can_ingest_given_docx_when_parsed_then_quotes(quotes_docx):
    quotes = Ingestor.parse(str(quotes_docx))
    assert quotes
    assert all([type(quote) == QuoteModel for quote in quotes])
