# Python Tic-Tac-Toe vs Computer

A feature-rich, command-line Tic-Tac-Toe game in Python where you can play against an AI opponent with customizable settings and difficulty levels.

## Features

- **3 AI Difficulties**:
  - **Easy**: Makes random moves. Great for casual play or beginners.
  - **Medium**: Plays tactically — seizes winning lines, blocks opponent wins, and controls the center.
  - **Hard (Unbeatable)**: Uses the **Minimax** decision algorithm with depth evaluation and alpha-beta pruning. It will never lose (optimal play leads to either an AI win or a draw).
- **Customizable Match Setup**:
  - Choose your symbol (`X` or `O`).
  - Choose who moves first (Player, Computer, or Random).
- **Visuals & UX**:
  - Clean numbered grid (1 to 9) showing available positions.
  - Color-coded markers and winning lines highlight (ANSI terminal colors).
  - Scoreboard tracking wins, losses, and draws across multiple rounds.
- **Robust Input Handling**:
  - Validates numeric inputs, handles out-of-range or occupied positions, and gracefully handles exits (`q` or Ctrl+C).

## Quick Start

### 1. Graphical Desktop App (Interactive Window)

A graphical window where you can click cells, switch difficulty, and track score:

```bash
python3 gui_game.py
```

### 2. Command-Line Terminal Interface

Run directly in your terminal:

```bash
python3 tic_tac_toe.py
```

### Board Layout

The board maps numbers `1` through `9` directly to the grid cells:

```text
 1 | 2 | 3 
---+---+---
 4 | 5 | 6 
---+---+---
 7 | 8 | 9 
```

To make a move, type the number corresponding to the cell and press `Enter`. Type `q` at any turn prompt to quit the current round.

## Running Tests

A comprehensive unit test suite is included in `test_game.py` covering game win/draw logic and verifying AI behavior:

```bash
python3 test_game.py
```
