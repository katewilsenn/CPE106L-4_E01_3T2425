import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # Specify the path to the IMDB.csv file (in the same folder as the script)
    csv_path = "IMDB.csv"  # Relative path (same directory as the script)

    # Check if the file exists
    if not os.path.exists(csv_path):
        print(f"Error: The file '{csv_path}' does not exist.")
        print(os.getcwd())
        return

    # Load the IMDB dataset from the CSV file
    moviesDF = pd.read_csv(csv_path)
    print("DataFrame loaded successfully:")
    print(moviesDF.head())

    # Ensure the 'Rating' column is numeric
    moviesDF['Rating'] = pd.to_numeric(moviesDF['Rating'], errors='coerce')

    # Group the data by 'Genre1' and calculate the average rating for each genre
    average_ratings = moviesDF.groupby('Genre1')['Rating'].mean()

    # Print the average ratings for debugging
    print("Average Ratings per Genre:")
    print(average_ratings)

    # Plot the data
    plt.figure(figsize=(10, 6))  # Set the figure size
    average_ratings.plot(kind='bar', color='skyblue')  # Create a bar plot


    # Add title and labels
    plt.title("Average Rating per Movie Genre")
    plt.xlabel("Genre")
    plt.ylabel("Average Rating")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Add a grid for better visualization
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Display the plot
    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.show()

# Call the main function
if __name__ == "__main__":
    main()
