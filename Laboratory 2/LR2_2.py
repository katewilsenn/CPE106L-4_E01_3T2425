def main():
    # Prompt user for filename and read all lines into a list
    file_name = input("Enter the file name: ")
    
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: File not found.")
        return

    if not lines:
        print("The file is empty.")
        return

    # Main loop for navigating lines
    while True:
        print(f"\nThe file has {len(lines)} lines.")
        try:
            line_number = int(input("Enter a line number (0 to quit): "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            continue

        if line_number == 0:
            print("Exiting the program.")
            break
        elif 1 <= line_number <= len(lines):
            print(f"Line {line_number}: {lines[line_number - 1].rstrip()}")
        else:
            print(f"Invalid line number. Please enter a number between 1 and {len(lines)}.")

if __name__ == "__main__":
    main()
