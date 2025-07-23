# test_commands.py
import unittest
from unittest.mock import patch
from InLab.oxo_cmd import Oxo_cmd

class TestCommands(unittest.TestCase):
    
    @patch('oxo_cmd.oxo_ui.playGame')  # Mock the playGame function to avoid GUI interaction
    def test_do_new(self, mock_play_game):
        cmd = Oxo_cmd()
        cmd.do_new("")
        mock_play_game.assert_called_once()  # Ensure playGame is called after starting a new game
    
    @patch('oxo_cmd.oxo_ui.playGame')  # Mock the playGame function again
    @patch('oxo_cmd.oxo_logic.restoreGame', return_value=[' '] * 9)  # Mock restoreGame
    def test_do_resume(self, mock_restore, mock_play_game):
        cmd = Oxo_cmd()
        cmd.do_resume("")
        mock_play_game.assert_called_once()  # Ensure playGame is called after resuming a game
    
    def test_do_quit(self):
        with self.assertRaises(SystemExit):
            cmd = Oxo_cmd()
            cmd.do_quit("")  # Ensure quit terminates the program
    
if __name__ == '__main__':
    unittest.main()
