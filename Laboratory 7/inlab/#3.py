import pandas as pd
import matplotlib.pyplot as plt

def main():
    moviesDF = pd.read_csv('IMDB.csv')
    moviesDF['Votes'] = moviesDF['Votes'].astype(str).str.replace(',', '')
    moviesDF['Votes'] = pd.to_numeric(moviesDF['Votes'], errors='coerce')
    drama_movies = moviesDF[moviesDF['Genre'].str.contains('Drama', na=False)]
    portion = drama_movies.loc[:, ['Title', 'Votes']]
    top_n = 10  # Show top 10 drama movies by votes
    portion = portion.sort_values(by='Votes', ascending=False).head(top_n)

    plt.figure(figsize=(12, 6))
    plt.bar(portion['Title'], portion['Votes'], color='skyblue')
    plt.xlabel('Movie Title')
    plt.ylabel('Number of Votes')
    plt.title('Top 10 Drama Movies by Votes')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()

if __name__ == "__main__":
    main()
