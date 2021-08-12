"""Manages meme generator."""

import os
import random

from quote_engine.ingestor import Ingestor
from quote_engine import QuoteModel
from meme_engine.engine import MemeEngine
from parser import parse_args
from errors import NoImagesFoundError


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./meme_generator/_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]
        try:
            img = random.choice(imgs)
        except IndexError as exc:
            raise NoImagesFoundError(
                f"No images found in path set by default: '{images}'")
    else:
        img = path

    if body is None:
        quote_files = ['./meme_generator/_data/DogQuotes/DogQuotesTXT.txt',
                       './meme_generator/_data/DogQuotes/DogQuotesDOCX.docx',
                       './meme_generator/_data/DogQuotes/DogQuotesPDF.pdf',
                       './meme_generator/_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    args = parse_args()
    print(generate_meme(args.path, args.body, args.author))
