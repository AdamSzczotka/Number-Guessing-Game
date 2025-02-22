import pytest
import json
import os


@pytest.fixture
def score_file():
    yield 'score_history.json'
    # Cleanup after tests
    if os.path.exists('score_history.json'):
        os.remove('score_history.json')


def test_update_high_score(score_manager):
    score_manager.update_high_score("easy", 100, "Player1")
    assert score_manager.high_score["easy"] == ("Player1", 100)

    # Test updating with better score
    score_manager.update_high_score("easy", 150, "Player2")
    assert score_manager.high_score["easy"] == ("Player2", 150)

    # Test not updating with worse score
    score_manager.update_high_score("easy", 90, "Player3")
    assert score_manager.high_score["easy"] == ("Player2", 150)


def test_save_score_history(score_manager, score_file):
    score_manager.high_score = {"easy": ("Player1", 100)}
    score_manager.save_score_history()

    assert os.path.exists(score_file)
    with open(score_file, 'r') as file:
        data = json.load(file)
        assert data == {"easy": ["Player1", 100]}


def test_load_score_history(score_manager, score_file):
    # Create test score file
    test_data = {"easy": ["Player1", 100]}
    with open(score_file, 'w') as file:
        json.dump(test_data, file)

    score_manager.load_score_history()
    assert score_manager.high_score == {"easy": ("Player1", 100)}


def test_load_score_history_no_file(score_manager):
    score_manager.load_score_history()
    assert score_manager.high_score == {}


def test_load_score_history_corrupted_file(score_manager, score_file):
    # Create corrupted file
    with open(score_file, 'w') as file:
        file.write("corrupted data")

    score_manager.load_score_history()
    assert score_manager.high_score == {}
