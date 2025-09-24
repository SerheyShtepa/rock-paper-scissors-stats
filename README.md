Rock Paper Scissors — GUI Version

A Python-based Rock-Paper-Scissors game with statistics tracking and a coin system. Built using Tkinter for GUI and Pandas for data management.

Features

Classic Rock-Paper-Scissors gameplay.

Player vs Computer rounds with coin betting:

Both start with 50 coins.

Each round costs 1 coin from both players, added to the bank.

Win → player receives all coins from bank.

Lose → computer receives all coins from bank.

Draw → coins remain in the bank.

Game over when player or computer runs out of coins.

Persistent game statistics saved in result.csv.

Total games, wins, losses, draws.

Win rate.

Most common player choice.

Pattern analysis for computer predictions (saved in pattern_stats.json).

GUI interface with buttons for moves, viewing stats, starting a new game, and exiting.

New Game button resets all coins and clears results.

Installation

Clone the repository:

git clone <repo_url>
cd rps-stats


Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows


Install dependencies:

pip install -r requirements.txt


Make sure tkinter is installed in your Python environment.
On Linux: sudo apt install python3-tk

Usage

Run the GUI:

python rps/gui.py


Click Rock, Paper, or Scissors to play a round.

Check the live stats and coin balances in the stats panel.

Double Click New Game to reset the game and start fresh.

Click Exit to close the application.

File Structure
rps-stats/
├── rps/
│   ├── game.py         # Main game logic
│   ├── stats.py        # Stats tracking functions
│   ├── gui.py          # GUI implementation
│   └── analyze.py      # Pattern analysis for AI
├── data/
│   ├── result.csv      # Game history
│   └── pattern_stats.json # Pattern analysis storage
├── tests/              # Pytest unit tests
├── requirements.txt
└── README.md

Testing

Run all tests using pytest:

pytest

Future Improvements

Add sound effects for wins/losses/draws.

Visual coin bank (progress bar or icons).

Difficulty levels for AI prediction.

Player profiles with persistent coins and stats.