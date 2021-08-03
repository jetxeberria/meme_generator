"""This module is a library of errors used in program."""


class NotImplementedError(Exception):
    """Error to be raised when reached a point of not implemented code."""


class InputNotSupportedError(Exception):
    """Error to be raised when input files extensions are not supported."""


class SystemProcessError(Exception):
    """Error to be raised when an operative system function fails."""


class OpeningFileError(SystemProcessError):
    """Error to be raised when opening a file fails using OS functions."""


class OutputFileError(SystemProcessError):
    """Error to be raised when can't process output file using OS functions."""


class NoImagesFoundError(Exception):
    """Error to be raised when can't found any image in searched path."""


class UrlReadError(Exception):
    """Error to be raised when can't request a given URL."""
