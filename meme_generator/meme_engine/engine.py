"""Module for meme generator."""

from os.path import join
from pathlib import PosixPath
from typing import Tuple

from PIL.Image import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL.JpegImagePlugin import JpegImageFile

from meme_generator.fileio import (build_random_filename,
                                   read_image, make_path)


class MemeEngine:
    """Combine images and text to create memes."""

    font_file = ("./_data/open-sans/OpenSans-Regular.ttf")

    def __init__(self, output_path: str):
        """Build a Meme Engine that saves memes in given directory."""
        self.output_path = make_path(output_path)

    def make_meme(
            self, img_path: str, body: str, author: str,
            width: int = 500) -> str:
        """Make a meme given a source image, a text body and an author."""
        img = read_image(img_path)
        body = body.strip("\"")
        author = author.strip()
        processed = self._process_image(img, width, body, author)
        source_img_name = PosixPath(img_path).stem
        output_meme = self._save_meme(processed, source_img_name)
        return output_meme

    def _process_image(
            self, image: JpegImageFile, width: int, body: str,
            author: str) -> Image:
        """Adjust size and add text to image."""
        resized = self._resize(image, width)
        draw = ImageDraw.Draw(resized)
        header_font = fit_header_font(body, resized.size, self.font_file)
        body_font = fit_footer_font(author, resized.size, self.font_file)
        img_W, img_H = resized.size
        header_w, _ = draw.textsize(body, font=header_font)
        body_w, body_h = draw.textsize(author, font=body_font)
        draw.text(((img_W-header_w)/2, 20),
                  body, fill="white", font=header_font)
        draw.text(((img_W-body_w)/2, img_H-body_h*2),
                  author, fill="white", font=body_font)
        return resized

    def _save_meme(self, image: Image, img_name: str):
        """Save meme image."""
        output_meme = self._build_meme_name(img_name)
        image.save(output_meme)
        return output_meme

    def _build_meme_name(self, img_name: str) -> str:
        """Build name for output meme."""
        meme_name = f"{img_name}_{build_random_filename()}.jpg"
        return join(self.output_path, meme_name)

    def _resize(self, img: JpegImageFile, width: int) -> Image:
        """Resize image to fix width."""
        reduction = width / img.width
        new_width, new_height = width, round(img.height * reduction)
        return img.resize((new_width, new_height))


def fit_text_font(
        text: str, size: Tuple[int, int], font_file: str,
        limit: int = None) -> ImageFont.FreeTypeFont:
    """Adjust font size to fit in a given size."""
    fontsize = 10
    write_area = size
    font = ImageFont.truetype(font_file, fontsize)
    while is_inside(font.getsize(text), write_area):
        fontsize += 1
        font = ImageFont.truetype(font_file, fontsize)
        if limit and limit != 0 and fontsize == limit:
            break
    return font


def is_inside(small_size: Tuple[int, int], big_size: Tuple[int, int]) -> bool:
    """Check whether first size is smaller than second one, in both axis."""
    if small_size[0] < big_size[0] and small_size[1] < big_size[1]:
        return True
    return False


def fit_header_font(
        text: str, size: Tuple[int, int], font: str) -> ImageFont.FreeTypeFont:
    """Adjust font size to fit in header section."""
    size = (round(size[0]*0.8), round(size[1]/2))
    return fit_text_font(text, size, font, limit=50)


def fit_footer_font(
        text: str, size: Tuple[int, int], font: str) -> ImageFont.FreeTypeFont:
    """Adjust font size to fit in footer section."""
    size = (round(size[0]), round(size[1]/4))
    return fit_text_font(text, size, font, limit=30)
