#!/usr/bin/env python3
"""
Tkinter GUI for Tic-Tac-Toe vs Computer
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Tuple

from tic_tac_toe import TicTacToe, ComputerAI


class TicTacToeGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tic-Tac-Toe vs Computer")
        self.root.resizable(False, False)

        # Game state
        self.game = TicTacToe()
        self.player_symbol = "X"
        self.ai_symbol = "O"
        self.difficulty_var = tk.StringVar(value="Hard")
        self.symbol_var = tk.StringVar(value="X")
        self.starter_var = tk.StringVar(value="Player")
        
        self.scores = {"player": 0, "ai": 0, "draw": 0}
        self.is_player_turn = True
        self.game_active = True

        self._configure_styles()
        self._build_ui()
        self.start_new_game()

    def _configure_styles(self) -> None:
        self.bg_color = "#f5f6fa"
        self.root.configure(bg=self.bg_color)

        self.font_title = ("Helvetica", 16, "bold")
        self.font_status = ("Helvetica", 13, "bold")
        self.font_score = ("Helvetica", 11)
        self.font_cell = ("Helvetica", 28, "bold")
        self.font_button = ("Helvetica", 11, "bold")

        self.color_x = "#2980b9"       # Deep blue
        self.color_o = "#c0392b"       # Crimson red
        self.color_win = "#27ae60"     # Emerald green
        self.color_cell_bg = "#ffffff"
        self.color_cell_active = "#dfe4ea"

        # Black button palette
        self.btn_primary_bg = "#000000"        # Solid black
        self.btn_primary_active = "#262626"    # Dark grey on active/hover
        self.btn_primary_fg = "#000000"        # Pitch black text
        self.btn_secondary_bg = "#000000"      # Solid black
        self.btn_secondary_active = "#262626"  # Dark grey on active/hover
        self.btn_secondary_fg = "#000000"      # Pitch black text
        self.btn_secondary_edge = "#000000"

    def _build_ui(self) -> None:
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=15)
        main_frame.pack()

        # Title & Subtitle
        title_label = tk.Label(
            main_frame,
            text="Tic-Tac-Toe",
            font=self.font_title,
            bg=self.bg_color,
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 5))

        # Settings panel
        settings_frame = tk.LabelFrame(
            main_frame,
            text=" Settings ",
            bg=self.bg_color,
            fg="#34495e",
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=6
        )
        settings_frame.pack(fill="x", pady=5)

        # Row 1: Symbol & Difficulty
        row1 = tk.Frame(settings_frame, bg=self.bg_color)
        row1.pack(fill="x", pady=2)

        tk.Label(row1, text="Play as:", bg=self.bg_color, font=self.font_score).pack(side="left")
        for sym in ["X", "O"]:
            tk.Radiobutton(
                row1,
                text=sym,
                value=sym,
                variable=self.symbol_var,
                command=self._on_settings_change,
                bg=self.bg_color,
                activebackground=self.bg_color,
                font=self.font_score
            ).pack(side="left", padx=4)

        tk.Label(row1, text="   Difficulty:", bg=self.bg_color, font=self.font_score).pack(side="left")
        diff_menu = ttk.Combobox(
            row1,
            textvariable=self.difficulty_var,
            values=["Easy", "Medium", "Hard"],
            state="readonly",
            width=8
        )
        diff_menu.pack(side="left", padx=4)
        diff_menu.bind("<<ComboboxSelected>>", lambda e: self._on_settings_change())

        # Row 2: Who goes first
        row2 = tk.Frame(settings_frame, bg=self.bg_color)
        row2.pack(fill="x", pady=2)
        tk.Label(row2, text="First move:", bg=self.bg_color, font=self.font_score).pack(side="left")
        for starter in ["Player", "Computer"]:
            tk.Radiobutton(
                row2,
                text=starter,
                value=starter,
                variable=self.starter_var,
                command=self._on_settings_change,
                bg=self.bg_color,
                activebackground=self.bg_color,
                font=self.font_score
            ).pack(side="left", padx=4)

        # Scoreboard Frame
        self.score_frame = tk.Frame(main_frame, bg="#e2e8f0", bd=1, relief="solid", padx=10, pady=6)
        self.score_frame.pack(fill="x", pady=8)

        self.score_label = tk.Label(
            self.score_frame,
            text="",
            font=self.font_score,
            bg="#e2e8f0",
            fg="#1e293b"
        )
        self.score_label.pack()
        self._update_score_display()

        # Status Banner
        self.status_label = tk.Label(
            main_frame,
            text="Your turn",
            font=self.font_status,
            bg=self.bg_color,
            fg="#2c3e50"
        )
        self.status_label.pack(pady=4)

        # 3x3 Board Grid
        board_frame = tk.Frame(main_frame, bg="#94a3b8", bd=3, relief="groove")
        board_frame.pack(pady=8)

        self.buttons: List[tk.Button] = []
        for i in range(9):
            row = i // 3
            col = i % 3
            btn = tk.Button(
                board_frame,
                text=" ",
                font=self.font_cell,
                width=3,
                height=1,
                bg=self.color_cell_bg,
                activebackground=self.color_cell_active,
                relief="flat",
                bd=0,
                command=lambda idx=i: self._handle_cell_click(idx)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.buttons.append(btn)

        # Control Buttons
        ctrl_frame = tk.Frame(main_frame, bg=self.bg_color)
        ctrl_frame.pack(fill="x", pady=8)

        self.btn_new_game = tk.Button(
            ctrl_frame,
            text="New Game",
            font=("Helvetica", 12, "bold"),
            bg=self.btn_primary_bg,
            fg=self.btn_primary_fg,
            activebackground=self.btn_primary_active,
            activeforeground=self.btn_primary_fg,
            highlightthickness=2,
            highlightbackground=self.btn_primary_bg,
            highlightcolor=self.btn_primary_active,
            padx=16,
            pady=7,
            bd=0,
            relief="flat",
            cursor="hand2",
            takefocus=True,
            command=self.start_new_game
        )
        self.btn_new_game.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.btn_reset_score = tk.Button(
            ctrl_frame,
            text="Reset Scores",
            font=("Helvetica", 12, "bold"),
            bg=self.btn_secondary_bg,
            fg=self.btn_secondary_fg,
            activebackground=self.btn_secondary_active,
            activeforeground=self.btn_secondary_fg,
            highlightthickness=2,
            highlightbackground=self.btn_secondary_edge,
            highlightcolor=self.btn_secondary_active,
            padx=16,
            pady=7,
            bd=0,
            relief="flat",
            cursor="hand2",
            takefocus=True,
            command=self.reset_scores
        )
        self.btn_reset_score.pack(side="right", expand=True, fill="x", padx=(8, 0))

        # Hover visual feedback
        self.btn_new_game.bind(
            "<Enter>",
            lambda e: self.btn_new_game.config(
                bg=self.btn_primary_active,
                highlightbackground=self.btn_primary_active
            )
        )
        self.btn_new_game.bind(
            "<Leave>",
            lambda e: self.btn_new_game.config(
                bg=self.btn_primary_bg,
                highlightbackground=self.btn_primary_bg
            )
        )
        self.btn_reset_score.bind(
            "<Enter>",
            lambda e: self.btn_reset_score.config(
                bg=self.btn_secondary_active,
                highlightbackground=self.btn_secondary_active
            )
        )
        self.btn_reset_score.bind(
            "<Leave>",
            lambda e: self.btn_reset_score.config(
                bg=self.btn_secondary_bg,
                highlightbackground=self.btn_secondary_bg
            )
        )

    def _on_settings_change(self) -> None:
        self.player_symbol = self.symbol_var.get()
        self.ai_symbol = "O" if self.player_symbol == "X" else "X"
        self.start_new_game()

    def _update_score_display(self) -> None:
        p_text = f"You ({self.player_symbol}): {self.scores['player']}"
        c_text = f"Computer ({self.ai_symbol}): {self.scores['ai']}"
        d_text = f"Draws: {self.scores['draw']}"
        self.score_label.config(text=f"{p_text}   |   {c_text}   |   {d_text}")

    def start_new_game(self) -> None:
        self.game.reset()
        self.game_active = True
        self.player_symbol = self.symbol_var.get()
        self.ai_symbol = "O" if self.player_symbol == "X" else "X"

        for btn in self.buttons:
            btn.config(text=" ", state="normal", bg=self.color_cell_bg)

        self._update_score_display()

        starter = self.starter_var.get()
        if starter == "Player":
            self.is_player_turn = True
            self.status_label.config(text=f"Your turn ({self.player_symbol})", fg="#2c3e50")
        else:
            self.is_player_turn = False
            self.status_label.config(text=f"Computer ({self.ai_symbol}) is thinking...", fg="#d97706")
            self.root.after(450, self._ai_turn)

    def _handle_cell_click(self, index: int) -> None:
        if not self.game_active or not self.is_player_turn:
            return

        if self.game.board[index] != " ":
            return

        # Player move
        self.game.make_move(index, self.player_symbol)
        self._update_cell_visual(index, self.player_symbol)

        if self._check_game_status():
            return

        # Computer turn
        self.is_player_turn = False
        self.status_label.config(text=f"Computer ({self.ai_symbol}) is thinking...", fg="#d97706")
        self.root.after(350, self._ai_turn)

    def _ai_turn(self) -> None:
        if not self.game_active:
            return

        ai = ComputerAI(
            ai_symbol=self.ai_symbol,
            player_symbol=self.player_symbol,
            difficulty=self.difficulty_var.get().lower()
        )
        ai_move = ai.get_move(self.game)
        self.game.make_move(ai_move, self.ai_symbol)
        self._update_cell_visual(ai_move, self.ai_symbol)

        if self._check_game_status():
            return

        self.is_player_turn = True
        self.status_label.config(text=f"Your turn ({self.player_symbol})", fg="#2c3e50")

    def _update_cell_visual(self, index: int, symbol: str) -> None:
        color = self.color_x if symbol == "X" else self.color_o
        self.buttons[index].config(text=symbol, fg=color)

    def _check_game_status(self) -> bool:
        winner = self.game.check_winner()
        winning_line = self.game.get_winning_line()

        if winner:
            self.game_active = False
            if winning_line:
                for idx in winning_line:
                    self.buttons[idx].config(bg="#bbf7d0", fg=self.color_win)

            if winner == self.player_symbol:
                self.scores["player"] += 1
                self.status_label.config(text="🎉 You won! Congratulations!", fg="#15803d")
            else:
                self.scores["ai"] += 1
                self.status_label.config(text="🤖 Computer won! Better luck next time.", fg="#b91c1c")

            self._update_score_display()
            return True

        if self.game.is_full():
            self.game_active = False
            self.scores["draw"] += 1
            self.status_label.config(text="🤝 It's a draw!", fg="#475569")
            self._update_score_display()
            return True

        return False

    def reset_scores(self) -> None:
        self.scores = {"player": 0, "ai": 0, "draw": 0}
        self._update_score_display()


def main() -> None:
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
