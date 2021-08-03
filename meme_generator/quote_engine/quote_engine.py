"""Manage the quotes."""


class QuoteModel:
    """Encapsulates a quote and her/his author."""

    def __init__(self, body: str, author: str):
        """Build a QuoteModel given a quote and author."""
        self.body = body
        self.author = author

    def __str__(self):
        """Humanly friendly print the object."""
        return f"\"{self.body}\" - {self.author}"
