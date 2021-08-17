"""Manages application hosting online."""

import random
import os
from flask import Flask, render_template, request

from quote_engine.ingestor import Ingestor
from meme_engine.engine import MemeEngine
from fileio import (system_remove_file, download_image)

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']
    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    meme_path = meme.make_meme(img, quote.body, quote.author)
    meme_path = get_path_from_static(meme_path)
    return render_template('meme.html', path=meme_path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    image_url = request.form['image_url']
    local_image = download_image(image_url)
    body = request.form['body']
    author = request.form['author']
    meme_path = meme.make_meme(local_image, body, author)
    meme_path = get_path_from_static(meme_path)
    system_remove_file(local_image)
    return render_template('meme.html', path=meme_path)


def main():
    """Run application."""
    app.run()


def get_path_from_static(path):
    """Discard parent directories of 'static' from path."""
    path = path.split("/")
    return "/".join(path[path.index("static"):])


if __name__ == "__main__":
    main()
