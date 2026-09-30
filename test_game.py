#!/usr/bin/env python3
"""
Unit tests for Tic-Tac-Toe and AI logic.
"""

import unittest
from tic_tac_toe import TicTacToe, ComputerAI


class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()

    def test_initial_board(self):
        self.assertEqual(len(self.game.available_moves()), 9)
        self.assertIsNone(self.game.check_winner())
        self.assertFalse(self.game.is_full())

    def test_row_win(self):
        self.game.make_move(0, "X")
        self.game.make_move(1, "X")
        self.game.make_move(2, "X")
        self.assertEqual(self.game.check_winner(), "X")
        self.assertTrue(self.game.is_game_over())

    def test_column_win(self):
        self.game.make_move(1, "O")
        self.game.make_move(4, "O")
        self.game.make_move(7, "O")
        self.assertEqual(self.game.check_winner(), "O")
        self.assertTrue(self.game.is_game_over())

    def test_diagonal_win(self):
        self.game.make_move(2, "X")
        self.game.make_move(4, "X")
        self.game.make_move(6, "X")
        self.assertEqual(self.game.check_winner(), "X")
        self.assertTrue(self.game.is_game_over())

    def test_draw(self):
        # Fill board without winner
        # X O X
        # X O O
        # O X X
        moves = [
            (0, "X"), (1, "O"), (2, "X"),
            (3, "X"), (4, "O"), (5, "O"),
            (6, "O"), (7, "X"), (8, "X")
        ]
        for pos, player in moves:
            self.game.make_move(pos, player)

        self.assertIsNone(self.game.check_winner())
        self.assertTrue(self.game.is_full())
        self.assertTrue(self.game.is_game_over())

    def test_invalid_move(self):
        self.assertTrue(self.game.make_move(0, "X"))
        # Cannot overwrite
        self.assertFalse(self.game.make_move(0, "O"))
        # Invalid indices
        self.assertFalse(self.game.make_move(-1, "X"))
        self.assertFalse(self.game.make_move(9, "X"))


class TestComputerAI(unittest.TestCase):
    def test_easy_ai(self):
        game = TicTacToe()
        ai = ComputerAI(ai_symbol="O", player_symbol="X", difficulty="easy")
        game.make_move(0, "X")
        move = ai.get_move(game)
        self.assertIn(move, game.available_moves())

    def test_medium_ai_wins_when_possible(self):
        game = TicTacToe()
        ai = ComputerAI(ai_symbol="O", player_symbol="X", difficulty="medium")
        # AI has (0, 1), should take 2 to win
        game.make_move(0, "O")
        game.make_move(1, "O")
        game.make_move(3, "X")
        game.make_move(4, "X")
        move = ai.get_move(game)
        self.assertEqual(move, 2)

    def test_medium_ai_blocks_opponent_win(self):
        game = TicTacToe()
        ai = ComputerAI(ai_symbol="O", player_symbol="X", difficulty="medium")
        # Player has (0, 4), threatens diagonal 8
        game.make_move(0, "X")
        game.make_move(1, "O")
        game.make_move(4, "X")
        move = ai.get_move(game)
        self.assertEqual(move, 8)

    def test_hard_ai_never_loses_against_random(self):
        # Run 50 simulated games with Hard AI vs Random Player
        import random
        for _ in range(50):
            game = TicTacToe()
            ai = ComputerAI(ai_symbol="O", player_symbol="X", difficulty="hard")
            
            # Random starting player
            turn = random.choice(["player", "ai"])
            while not game.is_game_over():
                if turn == "player":
                    rand_move = random.choice(game.available_moves())
                    game.make_move(rand_move, "X")
                    turn = "ai"
                else:
                    ai_move = ai.get_move(game)
                    game.make_move(ai_move, "O")
                    turn = "player"

            winner = game.check_winner()
            # Hard AI ('O') should never lose to random moves!
            self.assertNotEqual(winner, "X", f"Hard AI lost to random moves! Final board: {game.board}")

    def test_hard_ai_vs_hard_ai_always_draws(self):
        # Two optimal players must always end in a draw
        game = TicTacToe()
        ai_x = ComputerAI(ai_symbol="X", player_symbol="O", difficulty="hard")
        ai_o = ComputerAI(ai_symbol="O", player_symbol="X", difficulty="hard")

        turn = "X"
        while not game.is_game_over():
            if turn == "X":
                move = ai_x.get_move(game)
                game.make_move(move, "X")
                turn = "O"
            else:
                move = ai_o.get_move(game)
                game.make_move(move, "O")
                turn = "X"

        self.assertIsNone(game.check_winner(), f"Optimal vs optimal game was not a draw! Board: {game.board}")
        self.assertTrue(game.is_full())


if __name__ == "__main__":
    unittest.main()
