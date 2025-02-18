import pytest
import os
from number_guessing_game import GameSettings, ScoreManager, CLI


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


@pytest.fixture
def cli():
    return CLI()


def test_print_welcome_message(cli, capsys):
    cli.print_welcome_message()

    captured = capsys.readouterr()
    output = captured.out.strip()

    expected_output = ("Welcome to the Number Guessing Game!\n"
                       "Rules: Guess the number between 1 and 100. "
                       "You have limited attempts based on your "
                       "chosen difficulty.")
    assert output == expected_output


def test_get_player_name(cli, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "TestUser")

    player_name = cli.get_player_name()

    assert player_name == "TestUser"


@pytest.fixture
def score_manager():
    return ScoreManager()


def test_update_high_score(score_manager):
    score_manager.update_high_score("easy", 100, "Adam")
    assert score_manager.high_score["easy"] == ("Adam", 100)

    score_manager.update_high_score("easy", 123, "Jola")
    assert score_manager.high_score["easy"] == ("Jola", 123)

    score_manager.update_high_score("easy", 80, "Adam")
    assert score_manager.high_score["easy"] == ("Jola", 123)

    score_manager.update_high_score("medium", 100, "Adam")
    assert score_manager.high_score["medium"] == ("Adam", 100)

    score_manager.update_high_score("medium", 123, "Jola")
    assert score_manager.high_score["medium"] == ("Jola", 123)

    score_manager.update_high_score("medium", 80, "Adam")
    assert score_manager.high_score["medium"] == ("Jola", 123)

    score_manager.update_high_score("hard", 100, "Adam")
    assert score_manager.high_score["hard"] == ("Adam", 100)

    score_manager.update_high_score("hard", 123, "Jola")
    assert score_manager.high_score["hard"] == ("Jola", 123)

    score_manager.update_high_score("hard", 80, "Adam")
    assert score_manager.high_score["hard"] == ("Jola", 123)


def test_display_high_scores(score_manager, capsys):
    score_manager.update_high_score("easy", 100, "Adam")
    score_manager.update_high_score("medium", 120, "Jola")
    score_manager.update_high_score("hard", 130, "Bartek")

    score_manager.display_high_scores()

    captured = capsys.readouterr()
    output = captured.out.strip()

    expected_output = "High Scores: \nEasy: Adam - 100\nMedium: " \
                      "Jola - 120\nHard: Bartek - 130"
    assert output == expected_output


def test_save_score_history(score_manager):
    score_manager.update_high_score("easy", 100, "Adam")
    score_manager.save_score_history()

    # Check if file exist
    assert os.path.exists('score_history.json')


def test_load_score_history(score_manager):
    score_manager.update_high_score("easy", 100, "Adam")
    score_manager.save_score_history()
    # Load to new object
    new_manager = ScoreManager()
    new_manager.load_score_history()

    assert new_manager.high_score == score_manager.high_score

    # Clean test json file
    os.remove('score_history.json')


def test_load_score_history_no_file(score_manager):
    score_manager.load_score_history()

    assert score_manager.high_score == {}
