# AGENTS.md — Agent & Developer Guide

This document provides architectural context, codebase structure, design patterns, coding conventions, and operational workflows for AI agents and developers working on this repository.

---

## 1. What This Application Does

This project is a standalone, single-player **Tic-Tac-Toe** game against a computer opponent. It provides two user interfaces:
- **Terminal CLI** (`tic_tac_toe.py`): Interactive text-based game with ANSI color highlights, position overlays (1–9), score tracking across rounds, and robust input validation.
- **Desktop GUI** (`gui_game.py`): Tkinter-based graphical interface with interactive grid buttons, real-time status banners, dropdown difficulty selector, radio buttons for symbol/starter choices, and persistent scoreboard.

### Key Game Features
- **Symbol Selection**: Player can choose `X` (moves first by default) or `O` (moves second).
- **Turn Order**: Configurable first move: Player first, Computer first, or Random starter.
- **Difficulty Levels**:
  - `easy`: Pure random moves among available cells.
  - `medium`: Tactical rule-based heuristics (wins immediately if possible, blocks opponent wins, prioritizes center `4`, takes corners, then random).
  - `hard`: Unbeatable AI powered by the **Minimax** algorithm with depth-based score discounting (`10 - depth` for AI win, `depth - 10` for player win, `0` for draw) and alpha-beta pruning.
- **Score Tracking**: Persistent scoreboard tracking player wins, computer wins, and draws across matches.
- **Visual Feedback**: Winning 3-cell lines are identified and highlighted (green in terminal, light green background `#bbf7d0` with green text in GUI).

---

## 2. Tech Stack

- **Language**: Python 3 (compatible with Python 3.8+, tested on Python 3.14).
- **Core Dependencies**: **Zero external dependencies**; strictly relies on Python Standard Library modules:
  - `tkinter`, `tkinter.ttk`, `tkinter.messagebox` (Desktop UI)
  - `unittest` (Test suite)
  - `math`, `random`, `sys`, `os`, `time`, `typing`, `__future__.annotations` (Game logic, AI, CLI utilities)
- **Platforms**: macOS, Linux, and Windows (CLI includes fallback to disable ANSI colors if terminal does not support TTY/colors).

---

## 3. Folder Structure

```
/Users/pegz/Desktop/Game/
├── AGENTS.md           # Developer & agent orientation documentation (this file)
├── README.md           # Human-facing project overview and quick start guide
├── tic_tac_toe.py      # Core engine (TicTacToe, ComputerAI) and CLI application
├── gui_game.py         # Tkinter GUI implementation (TicTacToeGUI)
├── test_game.py        # Automated unit test suite using unittest
└── __pycache__/        # Python bytecode cache
```

---

## 4. Architectural Patterns & Code Structure

The project follows a modular **Model-View-Controller (MVC)**-style separation of concerns:

```
┌────────────────────────────────────────────────────────┐
│                        MODEL                           │
│  TicTacToe (tic_tac_toe.py)                            │
│  - Board state: List[str] length 9 (' ', 'X', 'O')     │
│  - make_move(), undo_move(), available_moves()         │
│  - check_winner(), is_full(), get_winning_line()       │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
┌─────────────────────────┐ ┌────────────────────────────┐
│      AI STRATEGY        │ │       VIEWS & CONTROLLERS  │
│  ComputerAI             │ │  CLI (tic_tac_toe.py)      │
│  - _easy_move()         │ │  - play_round(), main()    │
│  - _medium_move()       │ │  GUI (gui_game.py)         │
│  - _hard_move()         │ │  - TicTacToeGUI            │
│  - _minimax()           │ │  - Event-driven Tkinter UI │
└─────────────────────────┘ └────────────────────────────┘
```

### 1. Board Representation (`TicTacToe`)
- **Internal Storage**: `self.board: List[str]` of 9 items (`" "`, `"X"`, or `"O"`).
- **Indexing**: 0-indexed internally (`0` to `8`):
  ```
   0 | 1 | 2
  ---+---+---
   3 | 4 | 5
  ---+---+---
   6 | 7 | 8
  ```
- **Winning Combinations**: Defined in `TicTacToe.WINNING_COMBINATIONS` as tuples:
  - Rows: `(0, 1, 2)`, `(3, 4, 5)`, `(6, 7, 8)`
  - Columns: `(0, 3, 6)`, `(1, 4, 7)`, `(2, 5, 8)`
  - Diagonals: `(0, 4, 8)`, `(2, 4, 6)`
- **In-place Mutation & Backtracking**: Supports fast simulation via `make_move(pos, player)` and `undo_move(pos)`, enabling Minimax without cloning board objects.

### 2. AI Decision Engine (`ComputerAI`)
- Instantiated with `ai_symbol`, `player_symbol`, and `difficulty` string.
- Dispatches via `get_move(game: TicTacToe) -> int`:
  - `_easy_move`: Uses `random.choice(game.available_moves())`.
  - `_medium_move`: 1-ply search for immediate win, 1-ply search for opponent block, center preference (`4`), corner preference (`[0, 2, 6, 8]`), fallback random.
  - `_hard_move`: Opening move optimization (if board empty, picks corner/center randomly) followed by Minimax search with alpha-beta pruning.
  - `_minimax(game, depth, is_maximizing, alpha, beta)`: Recursively evaluates leaf states, penalizing longer paths so the AI wins as quickly as possible and defends as long as possible.

### 3. Frontends
- **CLI (`tic_tac_toe.py`)**:
  - `main()`: Outer loop handling setup (symbol, difficulty, first turn), round looping, score tracking, and restart confirmation.
  - `play_round()`: Turn-by-turn game loop managing player input validation, AI delay simulation (`time.sleep`), and game-over banner display.
  - User inputs are 1-indexed (`1`–`9`), converted to 0-indexed (`0`–`8`) positions internally.
- **GUI (`gui_game.py`)**:
  - `TicTacToeGUI`: Holds Tkinter root, `TicTacToe` instance, score dict, and UI widgets.
  - Asynchronous AI pacing: AI moves are triggered through `self.root.after(350, self._ai_turn)` so the UI redraws the player's move before freezing to compute.
  - Dynamic visual updates: Highlights winning row/col/diag in green (`#bbf7d0`).

---

## 5. Package Manager

- **No external package manager is used** (no `pip`, `poetry`, `pipenv`, `uv`, etc.).
- There is no `requirements.txt` or `pyproject.toml` because the project exclusively uses the standard library.
- When creating virtual environments or checking tools, use standard `python3 -m ...`.

---

## 6. Coding Conventions & Standards

When modifying or expanding the codebase, adhere to these existing project patterns:

1. **Type Annotations**:
   - Always include `from __future__ import annotations` at the top of Python files.
   - Use strict type hints for all function arguments and return values (`List`, `Optional`, `Tuple`, `int`, `str`, `bool`, etc.).
2. **Naming Conventions**:
   - Classes: `PascalCase` (`TicTacToe`, `ComputerAI`, `TicTacToeGUI`, `TestTicTacToe`).
   - Functions / Methods / Variables: `snake_case` (`make_move`, `available_moves`, `get_winning_line`).
   - Internal / Private Helpers: Leading underscore (`_easy_move`, `_ai_turn`, `_configure_styles`).
   - Constants: `UPPER_SNAKE_CASE` (`WINNING_COMBINATIONS`, `RESET`, `BOLD`, `CYAN`).
3. **Purity and Dependencies**:
   - Do **NOT** introduce third-party libraries (e.g. `pygame`, `numpy`, `rich`) unless specifically instructed. Keep the codebase lightweight and standard-library pure.
4. **Error Handling & Input Validation**:
   - Prompt input functions should handle `EOFError` and `KeyboardInterrupt` cleanly without dumping tracebacks.
   - CLI input loop must cleanly reject non-integer strings and out-of-range numbers with informative messages.
5. **UI Synchronization**:
   - Any new feature or configuration (e.g., a new difficulty mode) **must** be implemented symmetrically in:
     1. `tic_tac_toe.py` (CLI & `ComputerAI` logic)
     2. `gui_game.py` (GUI dropdowns/options)
     3. `test_game.py` (Unit test verification)
     4. `README.md` (User documentation)

---

## 7. How to Run the Project

### Graphical User Interface (GUI)
```bash
python3 gui_game.py
```

### Command-Line Interface (CLI)
```bash
python3 tic_tac_toe.py
```

---

## 8. How to Run Tests

The test suite is written using Python's standard `unittest` framework in `test_game.py`.

### Run tests directly:
```bash
python3 test_game.py
```

### Run tests via unittest runner with verbose output:
```bash
python3 -m unittest -v test_game.py
```

### Test Coverage Highlights:
- `TestTicTacToe`:
  - `test_initial_board`: Verifies 9 available moves, no winner, not full.
  - `test_row_win`, `test_column_win`, `test_diagonal_win`: Tests all winning vectors.
  - `test_draw`: Simulates a full board draw condition.
  - `test_invalid_move`: Verifies boundaries and prohibition against overwriting cells.
- `TestComputerAI`:
  - `test_easy_ai`: Verifies valid cell selection.
  - `test_medium_ai_wins_when_possible`: Checks immediate winning move execution.
  - `test_medium_ai_blocks_opponent_win`: Checks immediate threat blocking.
  - `test_hard_ai_never_loses_against_random`: Simulates 50 matches against random play; asserts AI never loses.
  - `test_hard_ai_vs_hard_ai_always_draws`: Plays two optimal Minimax bots against each other; asserts result is always a draw.

---

## 9. Important Constraints & Gotchas

1. **Board Coordinate Mapping**:
   - Users interact with **1-based** numbers `1` through `9`.
   - The board array is **0-based** indices `0` through `8`.
   - Ensure conversions (`pos = cell_num - 1` and `display = index + 1`) are preserved consistently across CLI, GUI, and tests.
2. **Minimax State Invariants**:
   - `ComputerAI._minimax` relies on in-place board modification (`game.make_move`) and backtracking (`game.undo_move`).
   - If writing new heuristics or search branches, ensure **every** `make_move` call is paired with an identical `undo_move` before returning.
3. **GUI Non-Blocking Execution**:
   - Tkinter runs on a single UI thread. Avoid blocking calls (like `time.sleep()`) in `gui_game.py` callbacks.
   - Use `self.root.after(milliseconds, callback)` to introduce pauses or schedule AI turns.
4. **Terminal Formatting**:
   - Check `sys.stdout.isatty()` before outputting ANSI sequences (`RESET`, `BOLD`, color codes). When piping or running non-interactively, ANSI formatting variables should remain empty strings.
