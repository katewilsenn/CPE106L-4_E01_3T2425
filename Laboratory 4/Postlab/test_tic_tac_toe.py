import unittest
from oxo_logic import TicTacToeGame

class TestTicTacToeGame(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToeGame()

    def test_new_game(self):
        self.assertEqual(self.game.board, [" "] * 9)

    def test_user_move(self):
        self.game.user_move(0)
        self.assertEqual(self.game.board[0], 'X')

    def test_invalid_user_move(self):
        self.game.user_move(0)
        with self.assertRaises(ValueError):
            self.game.user_move(0)

    def test_computer_move(self):
        self.game.computer_move()
        self.assertIn('O', self.game.board)

    def test_winning_move(self):
        self.game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertTrue(self.game._is_winning_move())

    def test_draw(self):
        self.game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'X']
        self.assertFalse(self.game._is_winning_move())
        self.assertEqual(self.game._generate_move(), -1)  # No more moves

if __name__ == "__main__":
    unittest.main()
