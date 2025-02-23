# Number Guessing Game 🎲

A classic number guessing game implemented in Python where players try to guess a randomly generated number within a limited number of attempts. The game features multiple difficulty levels, a hint system, and persistent high scores.

Project inspired by [Roadmap.sh Number Guessing Game](https://roadmap.sh/projects/number-guessing-game)

## Features 🌟

- Three difficulty levels (Easy, Medium, Hard)
- Hint system with limited hints per game
- Score tracking and persistence
- High score system
- Player statistics (games played, wins, win rate)
- Error handling and input validation
- Interactive CLI interface with emoji feedback

## Project Structure 📁

```
NUMBER-GUESSING-GAME
│
├── src/
│   ├── __init__.py
│   ├── number_guessing_game.py
│   └── score_history.json
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_game_manager.py
│   ├── test_game_round.py
│   ├── test_game_settings.py
│   ├── test_hint_system.py
│   ├── test_player.py
│   └── test_score_manager.py
│
├── .gitignore
├── LICENSE
├── pytest.ini
└── README.md
```

## Game Rules 📜

- Players must guess a number between 1 and 100
- Number of attempts depends on the chosen difficulty:
  - Easy: 10 attempts, 3 hints
  - Medium: 7 attempts, 2 hints
  - Hard: 5 attempts, 1 hint
- Score calculation considers:
  - Remaining attempts
  - Time taken to guess
  - Difficulty multiplier (Easy: 1x, Medium: 2x, Hard: 3x)
- Type 'hint' during gameplay to receive a helpful clue

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/AdamSzczotka/number-guessing-game.git
cd number-guessing-game
```

2. No additional dependencies are required as the game uses only Python standard library modules.

## Usage 🎮

Run the game from the project root directory:

```bash
python src/number_guessing_game.py
```

## Development 🛠️

### Running Tests

The project uses pytest for testing. To run the tests:

```bash
pytest
```

### Project Structure Overview

- `src/number_guessing_game.py`: Main game implementation with all game classes
- `src/score_history.json`: Persistent storage for high scores
- `tests/`: Complete test suite for all game components

## Classes Overview 📚

- `GameManager`: Main game controller
- `Player`: Handles player data and statistics
- `GameRound`: Manages individual game rounds
- `GameSettings`: Configures game difficulty and rules
- `CLI`: Handles all user interface interactions
- `ScoreManager`: Manages high score persistence
- `HintSystem`: Generates helpful hints during gameplay

## License 📄

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## Author ✍️

Adam Szczotka