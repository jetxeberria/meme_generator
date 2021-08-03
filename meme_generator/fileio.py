"""This module is a library of reading and writing methods."""

import random
import string
import subprocess
from os import makedirs

import csv
import requests
import json
from datetime import datetime
from typing import List, Any
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from docx import Document

from meme_generator.errors import (OpeningFileError,
                                   OutputFileError,
                                   SystemProcessError,
                                   UrlReadError)


def convert_pdf_to_txt(in_path: str, out_path: str = None) -> str:
    """Convert a file.pdf to a file.txt to be easily readable.

    Use unix system command 'pdftotext' to convert a file.pdf to a file.txt.
    Handles output code to raise error if operation not successful.

    Params
    ------
    in_path: [str] Input file path.
    output_path: [str, optional] Ouput file path.
    """
    if not out_path:
        out_path = "./tmp/"+build_random_filename()+".txt"
    status = subprocess.run(["mkdir", "./tmp"])
    status = subprocess.run(["pdftotext", in_path, out_path])
    if status.returncode == 1:
        raise OpeningFileError
    elif status.returncode == 2:
        raise OutputFileError
    elif status.returncode == 3:
        raise PermissionError

    return out_path


def build_random_filename(lenght: int = None) -> str:
    """Build random name letters-based with a given lenght, by default 5."""
    if not lenght:
        lenght = 5
    name = ''
    for n in range(lenght):
        name += random.choice(string.ascii_lowercase)
    return str(name)


def system_remove_file(filename: str) -> None:
    """Remove file from system using Unix 'rm' command."""
    status = subprocess.run(["rm", filename])
    if status.returncode != 0:
        raise SystemProcessError


def read_txt(filename: str) -> List[str]:
    """Read plain text (such as TXT) line by line given a filename path."""
    contents = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip("\n")
            if line and line not in string.whitespace:
                contents.append(line)
    return contents


def read_json(filename: str):
    """Read file as JSON given a filename path."""
    with open(filename, "r") as f:
        contents = json.load(f)
    return contents


def read_docx(filename: str) -> List[str]:
    """Read DOCX file given a filename path."""
    contents = []
    with open(filename, 'rb') as f:
        document = Document(f)
    for para in document.paragraphs:
        if para.text and para.text not in string.whitespace:
            contents.append(para.text)
    return contents


def read_csv(filename: str, header: bool = False) -> List[Any]:
    """Read CSV file given a filename path.

    Supports reading files with or without header. If header is provided,
    returns a dictionary for each line, else returns an ordered list for each
    line.
    """
    with open(filename, 'r') as f:
        contents = []
        if header:
            contents = list(csv.DictReader(f))
        else:
            reader = csv.reader(f)
            for line in reader:
                contents.append(line)
    return contents


def write_image(image: Image, filename: str) -> None:
    """Write image given filename."""
    image.save(filename)


def read_image(filename: str) -> JpegImageFile:
    """Read image given filename."""
    return Image.open(filename)


def make_path(path: str) -> str:
    """Build directory if missing."""
    try:
        makedirs(path)
    except FileExistsError as exc:
        print(f"'{path}' directory already exists. Skipping creation.")
    return path


def request_image(url: str):
    """Request an image from url."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise UrlReadError(f"Request to provided URL failed: '{url}'")
    return response.content


def save_image_with_datetime(image: Image) -> str:
    """Write an image with datetime."""
    now = datetime.now().isoformat(sep='_')
    random_name = f"./image{now}.jpg"
    with open(random_name, "wb") as f:
        f.write(image)
    return random_name


def download_image(image_url: str) -> str:
    """Download image from URL to local disk with datetime as filename."""
    image = request_image(image_url)
    filename = save_image_with_datetime(image)
    return filename
