"""
File: student.py
Resources to manage a student's name and test scores.
"""

import random
class Student(object):
    """Represents a student."""

    def __init__(self, name, number):
        """All scores are initially 0."""
        self.name = name
        self.scores = []
        for count in range(number):
            self.scores.append(0)

    def getName(self):
        """Returns the student's name."""
        return self.name
  
    def setScore(self, i, score):
        """Resets the ith score, counting from 1."""
        self.scores[i - 1] = score

    def getScore(self, i):
        """Returns the ith score, counting from 1."""
        return self.scores[i - 1]
    
    def getHighScore(self):
        """Returns the highest score."""
        return max(self.scores)
 
    def __str__(self):
        """Returns the string representation of the student."""
        return "Name: " + self.name + "\nScores: " + \
            " ".join(map(str, self.scores))

def main():
    names = ["Ran", "Kate", "Kara", "Angelo", "Aliyah"]
    students = []

    for name in names:
        student = Student(name, 5)
        scores = [random.randint(70, 100) for _ in range (5)]
        random.shuffle(scores)
        for i, score in enumerate(scores, 1):
            student.setScore(i, score)
        students.append(student)
    
    for student in students:
        print(student)
        print()

if __name__ == "__main__":
    main()