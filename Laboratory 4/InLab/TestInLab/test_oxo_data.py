# test_data.py
# test_data.py
import unittest
from unittest.mock import patch
import os
import InLab.oxo_data

class TestData(unittest.TestCase):
    
    @patch("oxo_data._getPath", return_value=os.getcwd())  # Mock the file path to avoid using the actual home directory
    def test_save_game(self, mock_get_path):
        game = ['X', 'O', ' ', ' ', 'X', ' ', ' ', ' ', 'O']
        InLab.oxo_data.saveGame(game)  # Save the game
        path = os.path.join(os.getcwd(), "oxogame.dat")
        self.assertTrue(os.path.exists(path))  # Ensure the file was created
    
    @patch("oxo_data._getPath", return_value=os.getcwd())  # Mock the file path again
    def test_restore_game(self, mock_get_path):
        game = ['X', 'O', ' ', ' ', 'X', ' ', ' ', ' ', 'O']
        InLab.oxo_data.saveGame(game)  # Save the game
        restored_game = InLab.oxo_data.restoreGame()  # Restore the game
        self.assertEqual(game, restored_game)  # Ensure the restored game is the same as the saved game
    
if __name__ == '__main__':
    unittest.main()
