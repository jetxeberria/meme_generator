"""Helpers for testing meme generator module."""

from pathlib import Path
from os.path import dirname

import pytest

PROJECT_PATH = dirname(__file__)
LESSON_HELPERS = Path(PROJECT_PATH)


@pytest.fixture
def quotes_pdf():
    """Return a path to an example PDF file."""
    return Path(LESSON_HELPERS, "DogQuotes", "DogQuotesPDF.pdf")


@pytest.fixture
def quotes_csv():
    """Return a path to an example CSV file."""
    return Path(LESSON_HELPERS, "DogQuotes", "DogQuotesCSV.csv")


@pytest.fixture
def quotes_txt():
    """Return a path to an example TXT file."""
    return Path(LESSON_HELPERS, "DogQuotes", "DogQuotesTXT.txt")


@pytest.fixture
def quotes_docx():
    """Return a path to an example DOCX file."""
    return Path(LESSON_HELPERS, "DogQuotes", "DogQuotesDOCX.docx")


@pytest.fixture
def photo_xander_1():
    """Return a path to an example JPG file."""
    return Path(LESSON_HELPERS, "photos", "dog", "xander_1.jpg")
