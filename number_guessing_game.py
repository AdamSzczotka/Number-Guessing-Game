# Autor: Adam Szczotka
# Title: Number guessing game

import time
import random
import json


class GameManager:
    def __init__(self):
        self.current_player = None
        self.game_settings = GameSettings()
        self.high_score = ScoreManager()
        self.is_game_running = True


class Player:
    pass


class GameRound:
    pass


class GameSettings:
    def __init__(self):
        self.difficulty_levels = {
            "easy": 10,
            "medium": 7,
            "hard": 5
        }
        self.number_range = (1, 100)
        self.hints_per_difficulty = {
            "easy": 3,
            "medium": 2,
            "hard": 1
        }
        self.score_multiplayer = {
            "easy": 1,
            "medium": 2,
            "hard": 3
        }

    def get_attempts(self, difficulty):
        return self.difficulty_levels[difficulty]

    def get_hints_allowed(self, difficulty):
        return self.hints_per_difficulty[difficulty]

    def get_score_multiplier(self, difficulty):
        return self.score_multiplayer[difficulty]


class CLI:
    pass


class ScoreManager:
    def __init__(self):
        self.high_score = {}
        self.score_history = {}

    def update_high_score(self, difficulty, score, player_name):
        if difficulty not in self.high_score or \
           self.high_score[difficulty][1] < score:
            self.high_score[difficulty] = (player_name, score)

    def display_high_scores(self):
        print("High Scores: ")
        for difficulty, (player, score) in self.high_score.items():
            print(f"{difficulty.capitalize()}: {player} - {score}")

    def save_score_history(self):
        with open('score_history.json', 'w') as file:
            json.dump(
                {key: list(value) for key, value in self.high_score.items()},
                file
            )

    def load_score_history(self):
        try:
            with open('score_history.json', 'r') as file:
                data = json.load(file)
                self.high_score = {
                    key: tuple(value) for key, value in data.items()
                    }
        except FileNotFoundError:
            self.high_score = {}


class HintSystem:
    pass


# Start the game
if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.start_game()
