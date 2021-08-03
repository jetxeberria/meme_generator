"""Manage the quotes."""


class QuoteEngine():
    """Don't know yet what does."""

    pass


class QuoteModel:
    """Encapsulates a quote and her/his author."""

    def __init__(self, body: str, author: str):
        """Build a QuoteModel given a quote and author."""
        self.body = body
        self.author = author
