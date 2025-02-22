

def test_game_settings_initialization(game_settings):
    assert game_settings.difficulty_levels == {
        "easy": 10,
        "medium": 7,
        "hard": 5
    }
    assert game_settings.number_range == (1, 100)
    assert game_settings.hints_per_difficulty == {
        "easy": 3,
        "medium": 2,
        "hard": 1
    }
    assert game_settings.score_multiplier == {
        "easy": 1,
        "medium": 2,
        "hard": 3
    }


def test_get_attempts(game_settings):
    assert game_settings.get_attempts("easy") == 10
    assert game_settings.get_attempts("medium") == 7
    assert game_settings.get_attempts("hard") == 5


def test_get_hints_allowed(game_settings):
    assert game_settings.get_hints_allowed("easy") == 3
    assert game_settings.get_hints_allowed("medium") == 2
    assert game_settings.get_hints_allowed("hard") == 1


def test_get_score_multiplier(game_settings):
    assert game_settings.get_score_multiplier("easy") == 1
    assert game_settings.get_score_multiplier("medium") == 2
    assert game_settings.get_score_multiplier("hard") == 3
