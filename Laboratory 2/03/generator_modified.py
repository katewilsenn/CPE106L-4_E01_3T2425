"""
Program: generator.py
Author: Ken (Modified)
Generates and displays sentences using a simple grammar
and vocabulary. Words are chosen at random from one file.
"""

import random

def getWords(filename):
    """Reads words from a file and returns them as a tuple."""
    try:
        with open(filename, 'r') as file:
            words = []
            for line in file:
                words.extend(line.strip().upper().split())
            return tuple(words)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return ()

# Load vocabulary from individual files
articles = getWords("articles.txt")
nouns = getWords("nouns.txt")
verbs = getWords("verbs.txt")
prepositions = getWords("prepositions.txt")

def sentence():
    """Builds and returns a sentence."""
    return nounPhrase() + " " + verbPhrase()

def nounPhrase():
    """Builds and returns a noun phrase."""
    return random.choice(articles) + " " + random.choice(nouns)

def verbPhrase():
    """Builds and returns a verb phrase."""
    return random.choice(verbs) + " " + nounPhrase() + " " + prepositionalPhrase()

def prepositionalPhrase():
    """Builds and returns a prepositional phrase."""
    return random.choice(prepositions) + " " + nounPhrase()

def main():
    """Prompts the user for the number of sentences to generate."""
    if not (articles and nouns and verbs and prepositions):
        print("Vocabulary loading failed. Exiting.")
        return

    try:
        number = int(input("Enter the number of sentences: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    for _ in range(number):
        print(sentence().capitalize() + ".")

# The entry point for program execution
if __name__ == "__main__":
    main()
