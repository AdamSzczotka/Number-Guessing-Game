

def test_game_round_initialization(game_round):
    assert game_round.difficulty_level == "medium"
    assert game_round.number_range == (1, 100)
    assert game_round.remaining_attempts == 7
    assert game_round.hints_remaining == 2
    assert game_round.is_won is False
    assert game_round.target_number is None


def test_generate_target_number(game_round):
    game_round.generate_target_number()
    assert 1 <= game_round.target_number <= 100


def test_process_guess_correct(game_round):
    game_round.generate_target_number()
    result = game_round.process_guess(game_round.target_number)
    assert result == "correct"
    assert game_round.remaining_attempts == 6


def test_process_guess_greater(game_round):
    game_round.target_number = 50
    result = game_round.process_guess(25)
    assert result == "greater"
    assert game_round.remaining_attempts == 6


def test_process_guess_less(game_round):
    game_round.target_number = 50
    result = game_round.process_guess(75)
    assert result == "less"
    assert game_round.remaining_attempts == 6


def test_provide_hint(game_round):
    game_round.target_number = 50
    hint = game_round.provide_hint()
    assert isinstance(hint, str)
    assert game_round.hints_remaining == 1


def test_no_hints_remaining(game_round):
    game_round.hints_remaining = 0
    hint = game_round.provide_hint()
    assert hint == "No hints left"


def test_check_game_over_attempts(game_round):
    game_round.remaining_attempts = 0
    assert game_round.check_game_over() is True


def test_check_game_over_won(game_round):
    game_round.is_won = True
    assert game_round.check_game_over() is True


def test_calculate_score(game_round):
    game_round.remaining_attempts = 5
    game_round.start_time = 100
    game_round.end_time = 120
    score = game_round.calculate_score(2)
    assert score == 980  # (5 * 2 * 100) - 20
