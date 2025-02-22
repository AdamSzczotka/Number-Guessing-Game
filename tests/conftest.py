import pytest
from number_guessing_game import GameManager, GameRound, Player, ScoreManager
from number_guessing_game import GameSettings


@pytest.fixture
def game_settings():
    return GameSettings()


@pytest.fixture
def player():
    return Player("TestPlayer")


@pytest.fixture
def score_manager():
    return ScoreManager()


@pytest.fixture
def game_manager():
    return GameManager()


@pytest.fixture
def game_round(game_settings):
    return GameRound(
        difficulty_level="medium",
        number_range=game_settings.number_range,
        attempts=game_settings.get_attempts("medium"),
        hints_remaining=game_settings.get_hints_allowed("medium")
    )
