import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_cli():
    with patch('number_guessing_game.CLI') as mock:
        yield mock


def test_start_game(mock_cli, game_manager):
    # Mock CLI responses
    mock_cli.get_player_name.return_value = "Test Player"
    mock_cli.play_again.side_effect = [False]  # Play once, then quit

    # Mock handle_game_round to do nothing
    game_manager.handle_game_round = MagicMock()

    # Mock high_score
    game_manager.high_score.load_score_history = MagicMock()
    game_manager.high_score.save_score_history = MagicMock()

    # Run the game
    game_manager.start_game()

    # Verify all expected methods were called
    mock_cli.print_welcome_message.assert_called_once()
    mock_cli.get_player_name.assert_called_once()
    assert game_manager.handle_game_round.call_count == 1
    mock_cli.play_again.assert_called_once()
    mock_cli.show_goodbye_message.assert_called_once()
    game_manager.high_score.load_score_history.assert_called_once()
    game_manager.high_score.save_score_history.assert_called_once()


def test_game_manager_initialization(game_manager):
    assert game_manager.current_player is None
    assert game_manager.is_game_running is True
    assert game_manager.game_settings is not None
    assert game_manager.high_score is not None


def test_handle_game_round_win(game_manager, mock_cli):
    # Setup
    game_manager.current_player = MagicMock()
    mock_cli.get_difficulty_choice.return_value = "medium"
    mock_cli.get_player_guess.side_effect = ["50"]  # Winning guess

    # Mock GameRound
    with patch('number_guessing_game.GameRound') as mock_round:
        instance = mock_round.return_value
        instance.target_number = 50
        instance.check_game_over.side_effect = [False, True]
        instance.process_guess.return_value = "correct"
        instance.is_won = True

        # Execute
        game_manager.handle_game_round()

        # Assert
        assert mock_cli.display_guess_result.called
        assert game_manager.current_player.update_stats.called
        assert mock_cli.display_game_stats.called


def test_handle_game_round_with_hint(game_manager, mock_cli):
    # Setup
    game_manager.current_player = MagicMock()
    mock_cli.get_difficulty_choice.return_value = "medium"
    mock_cli.get_player_guess.side_effect = ["hint", "50"]

    # Mock GameRound
    with patch('number_guessing_game.GameRound') as mock_round:
        instance = mock_round.return_value
        instance.target_number = 50
        instance.check_game_over.side_effect = [False, False, True]
        instance.process_guess.return_value = "correct"
        instance.provide_hint.return_value = "Test hint"
        instance.is_won = True

        # Execute
        game_manager.handle_game_round()

        # Assert
        assert mock_cli.show_hint.called
        assert mock_cli.display_guess_result.called


def test_handle_game_round_invalid_difficulty(game_manager, mock_cli):
    mock_cli.get_difficulty_choice.return_value = "invalid"

    game_manager.handle_game_round()

    assert mock_cli.show_error_message.called


def test_quit_game(game_manager, mock_cli):
    game_manager.quit_game()
    assert mock_cli.show_goodbye_message.called
