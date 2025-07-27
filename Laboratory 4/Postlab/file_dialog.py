import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def choose_file():
    """Open file dialog to choose a file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])
    return file_path

def read_file(file_path):
    """Read the file and return the lines as a list."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_path}' not found!")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def display_line(lines, line_number):
    """Display the line specified by line_number."""
    if line_number == 0:
        return False  # Exit condition
    if 1 <= line_number <= len(lines):
        messagebox.showinfo("Line Content", f"Line {line_number}: {lines[line_number - 1]}")
    else:
        messagebox.showwarning("Invalid Input", "The line number is out of range.")
    return True

def main():
    """Main function to drive the program."""
    file_path = choose_file()  # Let the user choose a file
    if not file_path:  # If no file was selected, exit the program
        return
    
    lines = read_file(file_path)  # Read the file into a list
    if not lines:
        return  # If the file couldn't be read, exit
    
    total_lines = len(lines)
    messagebox.showinfo("Total Lines", f"The file contains {total_lines} lines.")
    
    while True:
        # Ask the user for the line number they want to view
        line_number_input = simpledialog.askstring("Enter Line Number", 
                                                   f"Enter the line number (1-{total_lines}) to display, or 0 to quit:")
        
        if line_number_input is None:
            break  # User pressed Cancel on the dialog
        try:
            line_number = int(line_number_input)
            if line_number == 0:
                break  # Exit the loop if user enters 0
            if not display_line(lines, line_number):
                break  # Exit the loop if the line number is valid or 0
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()
