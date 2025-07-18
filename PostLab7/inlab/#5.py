
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # Specify the path to the Grades.csv file (in the same folder as the script)
    csv_path = "Grades.csv"  # Relative path (same directory as the script)

    # Check if the file exists
    if not os.path.exists(csv_path):
        print(f"Error: The file '{csv_path}' does not exist.")
        return

    # Load the data from the CSV file
    grades = pd.read_csv(csv_path)

    # Print the loaded data for debugging
    print("Loaded Grades Data:")
    print(grades.head())

    # Compute the total grade for each student
    grades['TotalGrade'] = grades.sum(axis=1)

    # Sort the DataFrame by TotalGrade in descending order
    grades.sort_values(by='TotalGrade', ascending=False, inplace=True)

    # Print the sorted DataFrame for debugging
    print("Sorted Grades Data:")
    print(grades)

    # Plot the problem scores for each student
    plt.figure(figsize=(12, 6))  # Set the figure size

    # Plot each problem score with a different color
    problems = grades.columns[:-1]  # Exclude the 'TotalGrade' column
    colors = ['b', 'g', 'r', 'c']  # Colors for each problem

    for i, problem in enumerate(problems):
        plt.plot(grades.index, grades[problem], 'o-', color=colors[i], label=problem)

    # Plot the total grade
    plt.plot(grades.index, grades['TotalGrade'], 'k--', label='Total Grade')

    # Add title and labels
    plt.title("Problem Scores and Total Grades for Each Student")
    plt.xlabel("Student Index")
    plt.ylabel("Score")

    # Add a legend
    plt.legend()

    # Add a grid for better visualization
    plt.grid(linestyle='--', alpha=0.7)

    # Display the plot
    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.show()

# Call the main function
if __name__ == "__main__":
    main()

