def main():
    filename = input("Enter filename: ")

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if not lines:
            print("The file is empty.")
            return

        total_lines = len(lines)
        print(f"The file has {total_lines} lines.")

        while True:
            try:
                line_number = int(input(f"Enter a line number (1 to {total_lines}, or 0 to quit): "))
                
                if line_number == 0:
                    print("Exiting program.")
                    break
                elif 1 <= line_number <= total_lines:
                    print(f"Line {line_number}: {lines[line_number - 1].rstrip()}")
                else:
                    print(f"Invalid input. Please enter a number from 1 to {total_lines}, or 0 to quit.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                
    except FileNotFoundError:
        print("File not found.")

if __name__ == "__main__":
    main()
