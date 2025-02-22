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

    def start_game(self):
        CLI.print_welcome_message()
        player_name = CLI.get_player_name()
        self.current_player = Player(player_name)
        self.high_score.load_score_history()


class Player:
    def __init__(self, name):
        self.name = name
        self.best_scores = {}
        self.total_games_played = 0
        self.total_wins = 0


class GameRound:
    def __init__(self, difficulty_level, number_range,
                 attempts, hints_remaining):
        self.target_number = None
        self.remaining_attempts = attempts
        self.difficulty_level = difficulty_level
        self.number_range = number_range
        self.start_time = time.time()
        self.end_time = None
        self.hints_remaining = hints_remaining
        self.current_score = 0
        self.is_won = False

    def generate_target_number(self):
        self.target_number = random.randint(*self.number_range)

    def process_guess(self, guess):
        self.remaining_attempts -= 1
        if guess == self.target_number:
            self.end_time = time.time()
            return "correct"
        elif guess < self.target_number:
            return "greater"
        elif guess > self.target_number:
            return "less"

    def calculate_score(self, multiplayer):
        duration = self.get_round_duration()
        return max(0, (self.remaining_attempts * multiplayer) - int(duration))

    def get_round_duration(self):
        return (self.end_time or time.time()) - self.start_time


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
    @staticmethod
    def print_welcome_message():
        print("Welcome to the Number Guessing Game!")
        print("Rules: Guess the number between 1 and 100. "
              "You have limited attempts based on your chosen difficulty.")

    @staticmethod
    def get_player_name():
        return input("Enter your name: ")


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
