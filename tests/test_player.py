

def test_player_initialization(player):
    assert player.name == "TestPlayer"
    assert player.total_games_played == 0
    assert player.total_wins == 0
    assert player.best_scores == {}


def test_update_stats_win(player, game_round):
    game_round.is_won = True
    game_round.remaining_attempts = 5
    game_round.start_time = 100
    game_round.end_time = 120

    player.update_stats(game_round)

    assert player.total_games_played == 1
    assert player.total_wins == 1
    assert player.best_scores["medium"] == 480  # (5 * 1 * 100) - 20


def test_update_stats_better_score(player, game_round):
    # First game
    game_round.is_won = True
    game_round.remaining_attempts = 3
    game_round.start_time = 100
    game_round.end_time = 110
    player.update_stats(game_round)

    # Second game with better score
    game_round.remaining_attempts = 5
    game_round.start_time = 200
    game_round.end_time = 210
    player.update_stats(game_round)

    assert player.total_games_played == 2
    assert player.total_wins == 2
    assert player.best_scores["medium"] == 490  # Better score is kept


def test_get_best_score(player):
    player.best_scores["easy"] = 100
    assert player.get_best_score("easy") == 100
    assert player.get_best_score("hard") is None
