
"""Test flask app."""

import pytest

from meme_generator.app import main


@pytest.mark.skip(reason="Manual test to run server app.")
def test_run_app_given_app_when_run_then_rendered():
    main()
    assert 0
