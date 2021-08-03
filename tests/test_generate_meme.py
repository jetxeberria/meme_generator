"""Test for generate_meme module."""

from pathlib import Path

from meme_generator.meme import generate_meme
from tests.helpers.helpers import photo_xander_1


def test_generate_meme_g_photo_w_make_then_saved(
        photo_xander_1):
    body = "Hi, are you fine?"
    author = "Me asw be"
    meme = generate_meme(photo_xander_1, body, author)
    assert Path(meme).is_file()


def test_generate_meme_g_photo_as_text_w_make_then_saved(
        photo_xander_1):
    body = "Hi, are you fine? This a rarely large quote"
    author = "Me asw be"
    photo = str(photo_xander_1)
    meme = generate_meme(photo, body, author)
    assert Path(meme).is_file()


def test_generate_meme_g_photo_no_body_no_author_w_make_then_random(
        photo_xander_1):
    photo = str(photo_xander_1)
    meme = generate_meme(photo)
    assert Path(meme).is_file()


def test_generate_meme_g_no_photo_no_body_no_author_w_make_then_random():
    meme = generate_meme()
    assert Path(meme).is_file()
