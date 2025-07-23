"""
  LAB 07
  PROGRAMMING PROBLEM 02

	The columns labeled FG, 3PT, and FT of the data set in the Analyzing Basketball Statistics case study (Download the files here >> CaseStudy2) do not show a single integer value but instead show values with the format <makes-attempts>, which is not suitable for the kind of data analysis performed on the other columns. For example, analysts might like to view the mean of free throws attempted as well as mean of the free throw percentage. You can correct this problem with a cleaning step that, for each such column:
    •	removes it from the data frame
    •	creates two new columns from this series, where the first column includes the numbers of makes and the second column includes the number of attempts
    •	inserts the new pairs of columns into the data frame at the appropriate positions, with the appropriate column headings (for example, FTM and FTA)
	Define a function named cleanStats in the file hoopstatsapp.py. This function expects a data frame as an argument and returns the frame cleaned according to the steps listed previously. You should call this function after the frame is loaded from the CSV file and before it is passed to the HoopStatsView constructor.
"""

"""
File: hoopstatsapp.py

The application for analyzing basketball stats.
"""

from hoopstatsview import HoopStatsView
import pandas as pd

def cleanStats(df):
    # Define the columns to be split
    columns_to_split = ['FG', '3PT', 'FT']
    
    for col in columns_to_split:
        if col in df.columns:
            # Split the column into makes and attempts
            makes_attempts = df[col].str.split('-', expand=True)
            df[f'{col}M'] = pd.to_numeric(makes_attempts[0], errors='coerce')  # Makes
            df[f'{col}A'] = pd.to_numeric(makes_attempts[1], errors='coerce')  # Attempts
            
            # Remove the original column
            df.drop(columns=[col], inplace=True)
    
    return df

def main():
    """Creates the data frame and view and starts the app."""
    try:
        frame = pd.read_csv("cleanbrogdonstats.csv")
        print("CSV file loaded successfully.")
        frame = cleanStats(frame)  # Clean the data before passing it to the view
        print("Data cleaned successfully.")
        print(frame.head())  # Print the first few rows of the DataFrame for verification
        HoopStatsView(frame)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
