import pytest
from number_guessing_game import GameSettings


@pytest.fixture
def game_settings():
    return GameSettings()


def test_game_attempts(game_settings):
    assert game_settings.get_attempts("easy") == 10
    assert game_settings.get_attempts("medium") == 7
    assert game_settings.get_attempts("hard") == 5


def test_game_hints_allowed(game_settings):
    assert game_settings.get_hints_allowed("easy") == 3
    assert game_settings.get_hints_allowed("medium") == 2
    assert game_settings.get_hints_allowed("hard") == 1


def test_get_score_multiplier(game_settings):
    assert game_settings.get_score_multiplier("easy") == 1
    assert game_settings.get_score_multiplier("medium") == 2
    assert game_settings.get_score_multiplier("hard") == 3
