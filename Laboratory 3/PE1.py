"""
File: student.py
Resources to manage a student's name and test scores.
"""

class Student(object):
    """Represents a student."""

    def __init__(self, name, number):
        """All scores are initially 0."""
        self.name = name
        self.scores = [0] * number

    def getName(self):
        """Returns the student's name."""
        return self.name
  
    def setScore(self, i, score):
        """Resets the ith score, counting from 1."""
        if 1 <= i <= len(self.scores):
            self.scores[i - 1] = score
        else:
            raise IndexError("Score index out of range.")

    def getScore(self, i):
        """Returns the ith score, counting from 1."""
        if 1 <= i <= len(self.scores):
            return self.scores[i - 1]
        else:
            raise IndexError("Score index out of range.")

    def getAverageScore(self):
        """Returns the average score."""
        return sum(self.scores) / len(self.scores)
    
    def getHighScore(self):
        """Returns the highest score."""
        return max(self.scores)
 
    def __str__(self):
        """Returns the string representation of the student."""
        scores_str = " ".join(map(str, self.scores))
        return f"Name: {self.name}\nScores: {scores_str}"

    def __eq__(self, other):
        return self.getAverageScore() == other.getAverageScore()

    def __lt__(self, other):
        return self.getAverageScore() < other.getAverageScore()

    def __gt__(self, other):
        return self.getAverageScore() > other.getAverageScore()

def main():
    student1 = Student("Ran", 3)
    student2 = Student("Kate", 3)
    student3 = Student("Kara", 3)

    student1.setScore(1, 80)
    student1.setScore(2, 90)
    student1.setScore(3, 100)

    student2.setScore(1, 70)
    student2.setScore(2, 85)
    student2.setScore(3, 95)

    student3.setScore(1, 60)
    student3.setScore(2, 75)
    student3.setScore(3, 85)

    students = [student1, student2, student3]
    
    for student in students:
        print(student)
        print(f'{student.getAverageScore():.2f}')
        print(f"Highest Score: {student.getHighScore()}")
        print()

    print("Comparison Results:")
    print(f"{student1.name} == {student2.name}? {student1 == student2}")
    print(f"{student1.name} > {student2.name}? {student1 > student2}")
    print(f"{student3.name} < {student2.name}? {student3 < student2}")

if __name__ == "__main__":
    main()

    
