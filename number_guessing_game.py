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

        while self.is_game_running:
            self.handle_game_round()
            self.is_game_running = CLI.play_again()
        self.quit_game()

    def handle_game_round(self):
        try:
            difficulty = CLI.get_difficulty_choice(
                self.game_settings.difficulty_levels)
            if difficulty not in self.game_settings.difficulty_levels:
                raise ValueError("Invalid difficulty level")

            attempts = self.game_settings.get_attempts(difficulty)
            hints_allowed = self.game_settings.get_hints_allowed(difficulty)

            game_round = GameRound(difficulty, self.game_settings.number_range,
                                   attempts, hints_allowed)
            game_round.generate_target_number()

            while not game_round.check_game_over():
                try:
                    guess = CLI.get_player_guess()
                    if guess == "hint":
                        hint = game_round.provide_hint()
                        CLI.show_hint(hint)
                        continue

                    guess = int(guess)
                    if not (self.game_settings.number_range[0] <= guess <=
                            self.game_settings.number_range[1]):
                        raise ValueError(
                            f"Guess must be between "
                            f"{self.game_settings.number_range[0]} and "
                            f"{self.game_settings.number_range[1]}")
                    result = game_round.process_guess(guess)
                    CLI.display_guess_result(result, game_round.target_number)
                    if result == "correct":
                        game_round.is_won = True
                        game_round.end_time = time.time()
                        self.current_player.update_stats(game_round)
                        score = game_round.calculate_score(
                            self.game_settings.get_score_multiplier(difficulty)
                        )
                        self.high_score.update_high_score(
                            difficulty, score, self.current_player.name
                        )
                        break
                except ValueError as e:
                    CLI.show_error_message(str(e))
                    continue

            if not game_round.is_won:
                CLI.display_guess_result("lost", game_round.target_number)

            CLI.display_game_stats(self.current_player, self.high_score)
        except ValueError as e:
            CLI.show_error_message(str(e))

    def quit_game(self):
        self.high_score.save_score_history()
        CLI.show_error_message("Thank you for playing! Goodbye!")


class Player:
    def __init__(self, name):
        self.name = name
        self.best_scores = {}
        self.total_games_played = 0
        self.total_wins = 0

    def update_stats(self, game_round):
        self.total_games_played += 1
        if game_round.is_won:
            self.total_wins += 1
            if (game_round.difficulty_level not in self.best_scores or
                self.best_scores[game_round.difficulty_level] >
                    game_round.remaining_attempts):
                self.best_scores[game_round.difficulty_level] = \
                    game_round.remaining_attempts

    def get_best_score(self, difficulty):
        return self.best_scores.get(difficulty, None)


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

    def provide_hint(self):
        if self.hints_remaining > 0:
            self.hints_remaining -= 1
            return HintSystem.generate_hint(self.target_number)
        return "No hints left"

    def check_game_over(self):
        return self.remaining_attempts <= 0 or self.is_won


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

    @staticmethod
    def get_difficulty_choice(difficulty_levels):
        print("Select difficulty:")
        for level in difficulty_levels:
            print(f"- {level} ({difficulty_levels[level]} attempts)")
        return input("Your choice: ").lower()

    @staticmethod
    def get_player_guess():
        return int(input("Enter your guess: "))

    @staticmethod
    def display_guess_result(result, target_number):
        if result == "correct":
            print("Congratulations! You guessed the correct number!")
        elif result == "greater":
            print("The number is greater than your guess.")
        elif result == "less":
            print("The number is less than your guess.")
        elif result == "lost":
            print(f"Game over! The correct number was {target_number}.")

    @staticmethod
    def display_game_stats(player, high_scores):
        print(f"Player: {player.name}, Games Played: "
              "{player.total_games_played}, Wins: {player.total_wins}")
        high_scores.display_high_scores()

    @staticmethod
    def play_again():
        choice = input("Do you want to play again? (yes/no): ").lower()
        return choice == "yes"

    @staticmethod
    def show_hint(hint):
        print(f"Hint: {hint}")

    @staticmethod
    def show_error_message(message):
        print(message)


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
    @staticmethod
    def generate_hint(target_number):
        return f"The number is divisible by {
            random.choice([x for x in range(1, 11) if target_number % x == 0])
            }."


# Start the game
if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.start_game()
