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

    # Only sum columns that end with '_grade'
    grade_columns = [col for col in grades.columns if col.endswith('_grade')]
    grades['TotalGrade'] = grades[grade_columns].sum(axis=1)

    # Sort the DataFrame by TotalGrade in descending order
    grades.sort_values(by='TotalGrade', ascending=False, inplace=True)

    # Print the sorted DataFrame for debugging
    print("Sorted Grades Data:")
    print(grades)

    # Plot the problem scores for each student
    plt.figure(figsize=(12, 6))  # Set the figure size
    colors = plt.cm.tab10.colors  # Use matplotlib's tab10 colormap for up to 10 assignments
    for i, problem in enumerate(grade_columns):
        plt.plot(grades.index, grades[problem], 'o-', color=colors[i % len(colors)], label=problem)
    plt.plot(grades.index, grades['TotalGrade'], 'k--', label='Total Grade')
    plt.title("Problem Scores and Total Grades for Each Student")
    plt.xlabel("Student Index")
    plt.ylabel("Score")
    plt.legend()
    plt.grid(linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Boxplot for distribution of scores for each assignment
    plt.figure(figsize=(10, 6))
    plt.boxplot([grades[col].dropna() for col in grade_columns], labels=grade_columns)
    plt.xlabel('Assignment')
    plt.ylabel('Score')
    plt.title('Distribution of Scores for Each Assignment')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# Call the main function
if __name__ == "__main__":
    main()

