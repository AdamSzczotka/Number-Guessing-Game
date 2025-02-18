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
    pass


class CLI:
    pass


class ScoreManager:
    pass


class HintSystem:
    pass


# Start the game
if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.start_game()
