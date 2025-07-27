import tkinter as tk
import tkinter.messagebox as mb
import oxo_logic  # Import the logic module

top = tk.Tk()
game_instance = oxo_logic.TicTacToeGame()  # Create an instance of TicTacToeGame

def buildMenu(parent):
    menus = (
        ("File", (("New", evNew),
                  ("Resume", evResume),
                  ("Save", evSave),
                  ("Exit", evExit))),
        ("Help", (("Help", evHelp),
                  ("About", evAbout)))
    )
        
    menubar = tk.Menu(parent)
    for menu in menus:
        m = tk.Menu(parent)
        for item in menu[1]:
            m.add_command(label=item[0], command=item[1])
        menubar.add_cascade(label=menu[0], menu=m)

    return menubar

def evNew():
    """Start a new game."""
    global game_instance
    game_instance = oxo_logic.TicTacToeGame()  # Create a new game instance
    status['text'] = "Playing game"
    game2cells(game_instance.board)

def evResume():
    """Resume the last saved game."""
    global game_instance
    game_instance.restore_game()  # Restore the saved game
    status['text'] = "Playing game"
    game2cells(game_instance.board)

def evSave():
    """Save the current game."""
    game_instance.save_game()  # Save the current game
    mb.showinfo("Save", "Game saved successfully.")

def evExit():
    """Exit the game."""
    if status['text'] == "Playing game":
        if mb.askyesno("Quitting", "Do you want to save the game before quitting?"):
            evSave()
    top.quit()

def evHelp():
    """Display help information."""
    mb.showinfo("Help", '''
    File->New: Starts a new game of Tic-Tac-Toe
    File->Resume: Restores the last saved game and commences play
    File->Save: Saves the current game.
    File->Exit: Quits, prompts to save active game
    Help->Help: Shows this page
    Help->About: Shows information about the program and author
    ''')

def evAbout():
    """Display about information."""
    mb.showinfo("About", "Tic-Tac-Toe game GUI demo by Alan Gauld")

def evClick(row, col):
    """Handle cell click for user move."""
    if status['text'] == "Game over":
        mb.showerror("Game over", "Game over!")
        return

    index = (3 * row) + col
    try:
        result = game_instance.user_move(index)  # Make user move
        game2cells(game_instance.board)  # Update the board with the user move
    except ValueError:
        mb.showerror("Invalid move", "Cell is already occupied!")

    if not result:
        result = game_instance.computer_move()  # Make computer move
        game2cells(game_instance.board)  # Update the board with the computer move

    # Check if the game is over (Winner or Draw)
    if result == "D":
        mb.showinfo("Result", "It's a Draw!")
        status['text'] = "Game over"
    elif result == "X" or result == "O":
        mb.showinfo("Result", f"The winner is: {result}")
        status['text'] = "Game over"

def game2cells(game):
    """Update the cells with the current game state."""
    table = board.pack_slaves()[0]
    for row in range(3):
        for col in range(3):
            table.grid_slaves(row=row, column=col)[0]['text'] = game[3 * row + col]

def cells2game():
    """Convert cells to game state."""
    values = []
    table = board.pack_slaves()[0]
    for row in range(3):
        for col in range(3):
            values.append(table.grid_slaves(row=row, column=col)[0]['text'])
    return values

def buildBoard(parent):
    """Build the game board."""
    outer = tk.Frame(parent, border=2, relief="sunken")
    inner = tk.Frame(outer)
    inner.pack()

    for row in range(3):
        for col in range(3):
            cell = tk.Button(inner, text=" ", width="5", height="2", 
                             command=lambda r=row, c=col: evClick(r, c))
            cell.grid(row=row, column=col)
    return outer

mbar = buildMenu(top)
top["menu"] = mbar

board = buildBoard(top)
board.pack()

status = tk.Label(top, text="Playing game", border=0, background="lightgrey", foreground="red")
status.pack(anchor="s", fill="x", expand=True)

tk.mainloop()
