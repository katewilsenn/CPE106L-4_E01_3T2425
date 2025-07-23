import pandas as pd  # Import pandas library
import matplotlib.pyplot as plt

def main():
    moviesDF = pd.read_csv('IMDB.csv')
    moviesDF.TotalVotes = moviesDF.TotalVotes.str.replace(',','')
    moviesDF.TotalVotes = pd.to_numeric(moviesDF.TotalVotes)
    portion = moviesDF[moviesDF.Genre1=='Drama'].loc[:,('Title', 'TotalVotes')]
    portion.sort_values(by='TotalVotes', inplace = True)
    plt.plot(portion.Title, portion.TotalVotes, 'bo')
    positions,titleLabels = plt.xticks()
    plt.setp(titleLabels, rotation = 30, ha = 'right')
    plt.grid()
    plt.show()

# Call the main function
if __name__ == "__main__":
    main()
