# test_oxo_logic.py
import unittest
from InLab.oxo_logic import newGame, userMove, computerMove, _isWinningMove
import InLab.oxo_data
import os

def cleanup_saved_game():
    if os.path.exists("oxogame.dat"):
        os.remove("oxogame.dat")

def setUp(self):
    cleanup_saved_game()

def tearDown(self):
    cleanup_saved_game()

class TestGameLogic(unittest.TestCase):
    
    def test_new_game(self):
        game = newGame()
        self.assertEqual(game, [' '] * 9)
    
    def test_user_move_valid(self):
        game = newGame()
        result = userMove(game, 0)  # 'X' moves to cell 0
        self.assertEqual(game[0], 'X')
        self.assertEqual(result, "")
    
    def test_user_move_invalid(self):
        game = newGame()
        userMove(game, 0)
        with self.assertRaises(ValueError):
            userMove(game, 0)  # Trying to move in an occupied cell
    
    def test_computer_move(self):
        game = newGame()
        result = computerMove(game)
        self.assertTrue(result in ["", "D", "O"])  # Should either be empty, draw, or 'O' wins
    
    def test_is_winning_move(self):
        game = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertTrue(_isWinningMove(game))  # Should return True for a horizontal win
    
    def test_save_game(self):
        game = newGame()
        InLab.oxo_data.saveGame(game)  # This will save the game to a file
        restored_game = InLab.oxo_data.restoreGame()  # This will restore the game from the file
        self.assertEqual(game, restored_game)  # The saved and restored game should be identical
    
if __name__ == '__main__':
    unittest.main()
