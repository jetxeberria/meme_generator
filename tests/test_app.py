
"""Test flask app."""

from meme_generator.app import main


def test_run_app_given_app_when_run_then_rendered():
    main()
    assert 0
