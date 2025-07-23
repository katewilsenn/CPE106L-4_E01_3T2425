def mean(numbers):
    """Returns the mean (average) of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def median(numbers):
    """Returns the median of a list of numbers."""
    if not numbers:
        return 0
    numbers = sorted(numbers)
    midpoint = len(numbers) // 2
    if len(numbers) % 2 == 1:
        return numbers[midpoint]
    else:
        return (numbers[midpoint - 1] + numbers[midpoint]) / 2


def mode(numbers):
    """Returns the mode of a list of numbers. If multiple modes, returns one of them."""
    if not numbers:
        return 0
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    for num, freq in frequency.items():
        if freq == max_freq:
            return num


def main():
    user_input = input("Enter numbers separated by spaces: ")
    try:
        numbers = [float(num) for num in user_input.split()]
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    print("Data:", numbers)
    print("Mean:", mean(numbers))
    print("Median:", median(numbers))
    print("Mode:", mode(numbers))


if __name__ == "__main__":
    main()
