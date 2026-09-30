#!/usr/bin/env python3
"""
Tic-Tac-Toe vs Computer
Features:
- Multiple difficulty levels: Easy, Medium, and Hard (Unbeatable Minimax).
- Customizable player symbol (X or O) and turn order.
- Clear board display with position guides and ANSI colors.
- Persistent score tracking across rounds.
"""

from __future__ import annotations

import math
import os
import random
import sys
import time
from typing import List, Optional, Tuple

# Terminal color constants
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"

# Disable colors if terminal does not support it
if not sys.stdout.isatty() or os.name == "nt" and "WT_SESSION" not in os.environ:
    RESET = BOLD = DIM = CYAN = GREEN = YELLOW = RED = BLUE = MAGENTA = ""


class TicTacToe:
    WINNING_COMBINATIONS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]

    def __init__(self) -> None:
        # Board represented by a list of 9 elements: ' ', 'X', or 'O'
        self.board: List[str] = [" "] * 9

    def reset(self) -> None:
        """Reset the board to empty."""
        self.board = [" "] * 9

    def available_moves(self) -> List[int]:
        """Return list of available cell indices (0-8)."""
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def make_move(self, position: int, player: str) -> bool:
        """Place player mark at position (0-8) if valid."""
        if 0 <= position < 9 and self.board[position] == " ":
            self.board[position] = player
            return True
        return False

    def undo_move(self, position: int) -> None:
        """Undo a move at position (0-8)."""
        self.board[position] = " "

    def check_winner(self) -> Optional[str]:
        """Return 'X' or 'O' if someone has won, otherwise None."""
        for a, b, c in self.WINNING_COMBINATIONS:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_full(self) -> bool:
        """Check if board is completely filled."""
        return " " not in self.board

    def is_game_over(self) -> bool:
        """Check if the game is over (win or draw)."""
        return self.check_winner() is not None or self.is_full()

    def get_winning_line(self) -> Optional[Tuple[int, int, int]]:
        """Return the tuple of indices that form the winning line, if any."""
        for combo in self.WINNING_COMBINATIONS:
            a, b, c = combo
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return combo
        return None


class ComputerAI:
    def __init__(self, ai_symbol: str, player_symbol: str, difficulty: str = "hard") -> None:
        self.ai = ai_symbol
        self.player = player_symbol
        self.difficulty = difficulty.lower()

    def get_move(self, game: TicTacToe) -> int:
        """Choose move based on difficulty."""
        available = game.available_moves()
        if not available:
            raise ValueError("No available moves left on the board.")

        if self.difficulty == "easy":
            return self._easy_move(available)
        elif self.difficulty == "medium":
            return self._medium_move(game, available)
        else:  # hard / unbeatable
            return self._hard_move(game)

    def _easy_move(self, available: List[int]) -> int:
        """Random selection."""
        return random.choice(available)

    def _medium_move(self, game: TicTacToe, available: List[int]) -> int:
        """Tactical move: win if possible, block opponent win, take center, else random."""
        # 1. Check if AI can win in next move
        for move in available:
            game.make_move(move, self.ai)
            if game.check_winner() == self.ai:
                game.undo_move(move)
                return move
            game.undo_move(move)

        # 2. Check if player can win in next move and block
        for move in available:
            game.make_move(move, self.player)
            if game.check_winner() == self.player:
                game.undo_move(move)
                return move
            game.undo_move(move)

        # 3. Take center if available
        if 4 in available:
            return 4

        # 4. Take corners
        corners = [m for m in available if m in [0, 2, 6, 8]]
        if corners:
            return random.choice(corners)

        # 5. Fallback random
        return random.choice(available)

    def _hard_move(self, game: TicTacToe) -> int:
        """Optimal move using Minimax with depth penalty."""
        # If whole board is empty, pick randomly among best opening positions (corners/center)
        available = game.available_moves()
        if len(available) == 9:
            return random.choice([0, 2, 4, 6, 8])

        best_score = -math.inf
        best_moves: List[int] = []

        for move in available:
            game.make_move(move, self.ai)
            score = self._minimax(game, depth=0, is_maximizing=False, alpha=-math.inf, beta=math.inf)
            game.undo_move(move)

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves)

    def _minimax(self, game: TicTacToe, depth: int, is_maximizing: bool, alpha: float, beta: float) -> int:
        winner = game.check_winner()
        if winner == self.ai:
            return 10 - depth
        elif winner == self.player:
            return depth - 10
        elif game.is_full():
            return 0

        if is_maximizing:
            max_eval = -math.inf
            for move in game.available_moves():
                game.make_move(move, self.ai)
                eval_score = self._minimax(game, depth + 1, False, alpha, beta)
                game.undo_move(move)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in game.available_moves():
                game.make_move(move, self.player)
                eval_score = self._minimax(game, depth + 1, True, alpha, beta)
                game.undo_move(move)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval


def format_cell(cell: str, position_hint: int, winning_cells: Optional[Tuple[int, int, int]] = None) -> str:
    """Format single cell for display with styling."""
    is_winning = winning_cells is not None and position_hint - 1 in winning_cells

    if cell == "X":
        formatted = f"{BOLD}{GREEN}X{RESET}" if is_winning else f"{BOLD}{CYAN}X{RESET}"
    elif cell == "O":
        formatted = f"{BOLD}{GREEN}O{RESET}" if is_winning else f"{BOLD}{MAGENTA}O{RESET}"
    else:
        formatted = f"{DIM}{position_hint}{RESET}"

    return f" {formatted} "


def print_board(game: TicTacToe) -> None:
    """Display the 3x3 board."""
    winning_line = game.get_winning_line()
    cells = [format_cell(game.board[i], i + 1, winning_line) for i in range(9)]

    print()
    print(f" {cells[0]}|{cells[1]}|{cells[2]} ")
    print("----+----+----")
    print(f" {cells[3]}|{cells[4]}|{cells[5]} ")
    print("----+----+----")
    print(f" {cells[6]}|{cells[7]}|{cells[8]} ")
    print()


def clear_screen() -> None:
    """Clear terminal screen if supported."""
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def prompt_choice(prompt_text: str, valid_options: List[str]) -> str:
    """Prompt user until a valid option is provided."""
    options_lower = [opt.lower() for opt in valid_options]
    while True:
        try:
            choice = input(prompt_text).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game. Goodbye!")
            sys.exit(0)
        if choice in options_lower:
            return choice
        print(f"{RED}Invalid input. Please choose from: {', '.join(valid_options)}{RESET}")


def play_round(player_symbol: str, ai_symbol: str, difficulty: str, first_turn: str) -> str:
    """Play a single round. Returns 'player', 'ai', or 'draw'."""
    game = TicTacToe()
    ai = ComputerAI(ai_symbol=ai_symbol, player_symbol=player_symbol, difficulty=difficulty)
    current_turn = first_turn

    while not game.is_game_over():
        clear_screen()
        print(f"{BOLD}=== TIC-TAC-TOE ==={RESET}")
        print(f"You: {BOLD}{CYAN if player_symbol == 'X' else MAGENTA}{player_symbol}{RESET} | "
              f"Computer: {BOLD}{MAGENTA if ai_symbol == 'O' else CYAN}{ai_symbol}{RESET} "
              f"({difficulty.capitalize()} mode)")
        print_board(game)

        if current_turn == "player":
            print(f"Your turn ({player_symbol}). Enter cell number (1-9) or 'q' to quit:")
            while True:
                try:
                    user_input = input(">> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nGame aborted.")
                    sys.exit(0)

                if user_input.lower() == "q":
                    print("Quitting current match...")
                    return "quit"

                if not user_input.isdigit():
                    print(f"{RED}Please enter a number between 1 and 9.{RESET}")
                    continue

                cell_num = int(user_input)
                if not 1 <= cell_num <= 9:
                    print(f"{RED}Number must be between 1 and 9.{RESET}")
                    continue

                pos = cell_num - 1
                if not game.make_move(pos, player_symbol):
                    print(f"{RED}Cell {cell_num} is already taken! Choose another.{RESET}")
                    continue

                break
            current_turn = "ai"
        else:
            print(f"Computer ({ai_symbol}) is thinking...", end="", flush=True)
            time.sleep(0.4)
            ai_pos = ai.get_move(game)
            game.make_move(ai_pos, ai_symbol)
            current_turn = "player"

    # End of round display
    clear_screen()
    print(f"{BOLD}=== TIC-TAC-TOE - GAME OVER ==={RESET}")
    print_board(game)

    winner = game.check_winner()
    if winner == player_symbol:
        print(f"{BOLD}{GREEN}🎉 Congratulations! You won this round! 🎉{RESET}\n")
        return "player"
    elif winner == ai_symbol:
        print(f"{BOLD}{RED}🤖 Computer won this round! Better luck next time.{RESET}\n")
        return "ai"
    else:
        print(f"{BOLD}{YELLOW}🤝 It's a draw! Well played.{RESET}\n")
        return "draw"


def main() -> None:
    clear_screen()
    print(f"{BOLD}{CYAN}=========================================={RESET}")
    print(f"{BOLD}{CYAN}       WELCOME TO TIC-TAC-TOE CLI         {RESET}")
    print(f"{BOLD}{CYAN}=========================================={RESET}\n")

    # Step 1: Select Symbol
    print("Choose your symbol:")
    print("  [X] Goes first (traditional)")
    print("  [O] Goes second")
    symbol_choice = prompt_choice("Choose X or O (default X): ", ["x", "o", ""])
    player_symbol = "O" if symbol_choice == "o" else "X"
    ai_symbol = "X" if player_symbol == "O" else "O"

    # Step 2: Select Difficulty
    print("\nSelect difficulty level:")
    print("  [1] Easy   - Computer makes random moves")
    print("  [2] Medium - Computer blocks & seizes direct wins")
    print("  [3] Hard   - Unbeatable (Minimax algorithm)")
    diff_input = prompt_choice("Select difficulty (1/2/3): ", ["1", "2", "3"])
    diff_map = {"1": "easy", "2": "medium", "3": "hard"}
    difficulty = diff_map[diff_input]

    # Step 3: Choose who goes first
    print("\nWho should take the first turn?")
    print("  [1] Player first")
    print("  [2] Computer first")
    print("  [3] Random")
    turn_input = prompt_choice("Choose (1/2/3, default 1): ", ["1", "2", "3", ""])
    if turn_input == "2":
        default_starter = "ai"
    elif turn_input == "3":
        default_starter = "random"
    else:
        default_starter = "player"

    # Score tracking
    scores = {"player": 0, "ai": 0, "draw": 0}
    round_number = 1

    while True:
        if default_starter == "random":
            starter = random.choice(["player", "ai"])
        else:
            starter = default_starter

        print(f"\n--- Starting Round {round_number} ---")
        time.sleep(0.5)

        result = play_round(player_symbol, ai_symbol, difficulty, starter)
        if result == "quit":
            break

        scores[result] += 1

        # Display Scoreboard
        print(f"{BOLD}📊 SCOREBOARD:{RESET}")
        print(f"  Player ({player_symbol})   : {scores['player']}")
        print(f"  Computer ({ai_symbol}) : {scores['ai']}")
        print(f"  Draws        : {scores['draw']}")
        print("-" * 25)

        play_again = prompt_choice("Play another round? (y/n): ", ["y", "n", "yes", "no"])
        if play_again in ["n", "no"]:
            break

        round_number += 1

    print(f"\n{CYAN}Thanks for playing Tic-Tac-Toe! Final score:{RESET}")
    print(f"Player: {scores['player']} | Computer: {scores['ai']} | Draws: {scores['draw']}")
    print("Have a great day!\n")


if __name__ == "__main__":
    main()
