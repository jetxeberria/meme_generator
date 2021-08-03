"""Parser of arguments required by application."""
import argparse


def build_parser():
    """Create a parser to parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Make a meme given an image, a body and an author.")
    parser.add_argument(
        '--path', dest="path", default=None,
        help="Absolute or relative path to source image")
    parser.add_argument(
        '--body', dest="body", default=None,
        help="Sentence to appear as main body")
    parser.add_argument(
        '--author', dest="author", default=None,
        help="Author of the sentence")
    return parser


def parse_args():
    """Parse given arguments."""
    arg_parser = build_parser()
    return arg_parser.parse_args()
