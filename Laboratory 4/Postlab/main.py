from oxo_logic import TicTacToeGame
from file_dialog import choose_file

def main():
    # Initialize a new game
    game = TicTacToeGame()

    # Ask the user to choose a file for saving or loading
    file_path = choose_file()
    print("Selected file:", file_path)

    # Start the game play
    game.play_game()

if __name__ == "__main__":
    main()
