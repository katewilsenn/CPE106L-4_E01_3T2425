import random
import oxo_data

class TicTacToeGame:
    def __init__(self):
        self.board = self.new_game()
        self.winner = None

    def new_game(self):
        """Initialize a new empty game board."""
        return list(" " * 9)

    def save_game(self):
        """Save the current game to disk."""
        oxo_data.saveGame(self.board)

    def restore_game(self):
        """Restore a previously saved game. Return new game if restoration fails."""
        try:
            game = oxo_data.restoreGame()
            if len(game) == 9:
                self.board = game
            else:
                self.board = self.new_game()
        except IOError:
            self.board = self.new_game()

    def _generate_move(self):
        """Generate a random move from available cells."""
        options = [i for i in range(len(self.board)) if self.board[i] == " "]
        if options:
            return random.choice(options)
        else:
            return -1

    def _is_winning_move(self):
        """Check if the current state of the board is a winning move."""
        wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6))

        for a, b, c in wins:
            chars = self.board[a] + self.board[b] + self.board[c]
            if chars == 'XXX' or chars == 'OOO':
                return True
        return False

    def user_move(self, cell):
        """Handle the user's move. Check for validity and winning condition."""
        if self.board[cell] != ' ':
            raise ValueError('Invalid cell')
        else:
            self.board[cell] = 'X'
        if self._is_winning_move():
            self.winner = 'X'
        return self.winner

    def computer_move(self):
        """Generate a move for the computer and check for winning condition."""
        cell = self._generate_move()
        if cell == -1:
            self.winner = 'D'  # Draw if no moves are available
        self.board[cell] = 'O'
        if self._is_winning_move():
            self.winner = 'O'
        return self.winner

    def play_game(self):
        """Simulate the entire game play loop."""
        result = ""
        while not result:
            print(self.board)
            try:
                result = self.user_move(self._generate_move())
            except ValueError:
                print("Oops, that shouldn't happen.")
            if not result:
                result = self.computer_move()

            if not result:
                continue
            elif result == 'D':
                print("It's a draw")
            else:
                print("Winner is:", result)
            print(self.board)
