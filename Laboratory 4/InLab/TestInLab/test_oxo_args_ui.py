# test_args_ui.py
import unittest
from unittest.mock import patch
import sys
from InLab.oxo_args_ui import main

class TestArgsUI(unittest.TestCase):
    
    @patch('sys.argv', ['oxo_args_ui.py', '--new'])
    @patch('oxo_args_ui.executeChoice')
    def test_new_game_argument(self, mock_execute_choice):
        main()
        mock_execute_choice.assert_called_once_with(1)  # Simulate selecting option 1 (new game)
    
    @patch('sys.argv', ['oxo_args_ui.py', '--res'])
    @patch('oxo_args_ui.executeChoice')
    def test_resume_game_argument(self, mock_execute_choice):
        main()
        mock_execute_choice.assert_called_once_with(2)  # Simulate selecting option 2 (resume game)

if __name__ == '__main__':
    unittest.main()
