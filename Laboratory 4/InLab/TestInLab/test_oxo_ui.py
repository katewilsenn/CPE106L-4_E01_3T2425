import unittest
from unittest.mock import patch
from InLab.oxo_ui import getMenuChoice, startGame, resumeGame, displayHelp, quit

class TestUI(unittest.TestCase):
    
    @patch("builtins.input", side_effect=["1"])  # Simulate choosing menu option 1 (Start new game)
    def test_get_menu_choice(self, mock_input):
        result = getMenuChoice(["Option 1", "Option 2", "Option 3"])
        self.assertEqual(result, 1)
    
    def test_start_game(self):
        game = startGame()
        self.assertEqual(game, [' '] * 9)  # New game should return an empty board
    
    @patch("InLab.oxo_ui.oxo_logic.restoreGame", return_value=[' '] * 9)  # Mock restoreGame to return a new game
    def test_resume_game(self, mock_restore):
        game = resumeGame()
        self.assertEqual(game, [' '] * 9)
    
    def test_display_help(self):
        with patch("builtins.print") as mock_print:
            displayHelp()
            mock_print.assert_called_with(''' 
Start new game:  starts a new game of tic-tac-toe
Resume saved game: restores the last saved game and commences play
Display help: shows this page
Quit: quits the application
''')
    
    @patch("builtins.input", side_effect=["q"])  # Simulate quitting the game
    def test_quit(self, mock_input):
        with self.assertRaises(SystemExit):
            quit()
    
if __name__ == '__main__':
    unittest.main()
