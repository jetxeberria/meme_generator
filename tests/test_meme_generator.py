#!/usr/bin/env python

"""Tests for `meme_generator` package."""
import meme_generator

def test_package_publishes_version_info():
    """Tests that the `meme_generator` publishes the current verion"""

    assert hasattr(meme_generator, '__version__')
