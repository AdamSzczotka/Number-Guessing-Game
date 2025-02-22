import pytest
from unittest.mock import patch
import os
import time
import random
from number_guessing_game import GameManager, Player, GameRound
from number_guessing_game import GameSettings, CLI, ScoreManager


@pytest.fixture
def game_manager():
    return GameManager()


def test_start_game(game_manager):
    with patch.object(CLI, "print_welcome_message") as mock_print_welcome, \
         patch.object(CLI, "get_player_name", return_value="TestUser") \
         as mock_get_player_name:

        game_manager.start_game()

        mock_print_welcome.assert_called_once()

        mock_get_player_name.assert_called_once()

        assert game_manager.current_player is not None
        assert isinstance(game_manager.current_player, Player)
        assert game_manager.current_player.name == "TestUser"

        assert game_manager.is_game_running is True


@pytest.fixture
def game_round():
    return GameRound(difficulty_level="medium", number_range=(1, 100),
                     attempts=7, hints_remaining=2)


def test_generate_target_number(game_round):
    game_round.generate_target_number()

    assert game_round.target_number is not None
    assert 1 <= game_round.target_number <= 100


@pytest.fixture
def game_round_fixed():
    round_instance = GameRound(difficulty_level="medium",
                               number_range=(1, 100),
                               attempts=7, hints_remaining=2)
    round_instance.target_number = 50
    return round_instance


def test_process_guess_correct(game_round_fixed):
    result = game_round_fixed.process_guess(50)
    assert result == "correct"
    assert game_round_fixed.end_time is not None


def test_process_guess_greater(game_round_fixed):
    result = game_round_fixed.process_guess(30)
    assert result == "greater"
    assert game_round_fixed.remaining_attempts == 6


def test_process_guess_less(game_round_fixed):
    result = game_round_fixed.process_guess(70)
    assert result == "less"
    assert game_round_fixed.remaining_attempts == 6


def test_attempts_decrease(game_round_fixed):
    initial_attempts = game_round_fixed.remaining_attempts
    game_round_fixed.process_guess(20)
    assert game_round_fixed.remaining_attempts == initial_attempts - 1


def test_get_round_duration(game_round_fixed):
    game_round_fixed.end_time = game_round_fixed.start_time + 10
    duration = game_round_fixed.get_round_duration()
    assert duration == 10


def test_process_guess_edge_cases(game_round_fixed):
    result = game_round_fixed.process_guess(game_round_fixed.target_number)
    assert result == "correct"

    result = game_round_fixed.process_guess(9999)
    assert result == "less"

    result = game_round_fixed.process_guess(-9999)
    assert result == "greater"


def test_provide_hint(game_round_fixed):
    initial_hints = game_round_fixed.hints_remaining

    hint = game_round_fixed.provide_hint()
    assert hint is not None
    assert game_round_fixed.hints_remaining == initial_hints - 1

    # If no hints left
    game_round_fixed.hints_remaining = 0
    hint = game_round_fixed.provide_hint()
    assert hint == "No hints left"


# Testing check_game_over method
def test_check_game_over_no_attempts(game_round_fixed):
    game_round_fixed.remaining_attempts = 0
    assert game_round_fixed.check_game_over() is True


def test_check_game_over_won(game_round_fixed):
    game_round_fixed.is_won = True
    assert game_round_fixed.check_game_over() is True


def test_check_game_over_not_over(game_round_fixed):
    game_round_fixed.remaining_attempts = 3
    game_round_fixed.is_won = False
    assert game_round_fixed.check_game_over() is False


"""
# Testing is_won after correct guess
def test_is_won(game_round_fixed):
    game_round_fixed.process_guess(game_round_fixed.target_number)
    assert game_round_fixed.is_won is True
"""


@pytest.fixture
def game_round_with_score():
    round_instance = GameRound(difficulty_level="medium",
                               number_range=(1, 100),
                               attempts=7, hints_remaining=2)
    round_instance.target_number = 50  # For testing purposes
    round_instance.remaining_attempts = 5  # Simulate remaining attempts
    round_instance.end_time = time.time() + 5  # Simulate 5 seconds duration
    return round_instance


def test_calculate_score(game_round_with_score):
    multiplayer = 2
    score = game_round_with_score.calculate_score(multiplayer)

    expected_score = max(0, (5 * multiplayer) - 5)
    assert score == expected_score


def test_calculate_score_with_multiple_attempts(game_round_with_score):
    multiplayer = 2
    game_round_with_score.remaining_attempts = 3
    score = game_round_with_score.calculate_score(multiplayer)

    assert score == 1


def test_calculate_score_with_no_attempts(game_round_with_score):
    multiplayer = 2
    game_round_with_score.remaining_attempts = 0
    score = game_round_with_score.calculate_score(multiplayer)

    assert score == 0


def test_calculate_score_with_long_duration(game_round_with_score):
    multiplayer = 2
    game_round_with_score.end_time = game_round_with_score.start_time + 20
    score = game_round_with_score.calculate_score(multiplayer)

    assert score == 0


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


class HintSystem:
    @staticmethod
    def generate_hint(target_number):
        return f"The number is divisible by {
            random.choice([x for x in range(1, 11) if target_number % x == 0])
            }."


@patch('random.choice')
def test_generate_hint_divisible_by(mock_choice, game_round_fixed):
    mock_choice.return_value = 5
    game_round_fixed.target_number = 30
    hint = HintSystem.generate_hint(game_round_fixed.target_number)
    assert "5" in hint


def test_generate_hint_edge_case(game_round_fixed):
    game_round_fixed.target_number = 1

    hint = HintSystem.generate_hint(game_round_fixed.target_number)
    assert "1" in hint


@patch('random.choice')
def test_generate_hint_multiple_possible_divisors(mock_choice,
                                                  game_round_fixed):

    game_round_fixed.target_number = 60

    mock_choice.return_value = 5

    hint = HintSystem.generate_hint(game_round_fixed.target_number)

    assert "5" in hint


def test_generate_hint_invalid_divisor(game_round_fixed):
    game_round_fixed.target_number = 13

    hint = HintSystem.generate_hint(game_round_fixed.target_number)
    assert "1" in hint or "13" in hint
