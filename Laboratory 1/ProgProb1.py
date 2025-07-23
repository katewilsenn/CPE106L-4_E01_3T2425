def mean(numbers):
    """Return the mean (average) of the list of numbers."""
    if not numbers:
        raise ValueError("The list is empty.")
    return sum(numbers) / len(numbers)


def median(numbers):
    """Return the median (middle value) of the sorted list of numbers."""
    if not numbers:
        raise ValueError("The list is empty.")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2

    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        return sorted_nums[mid]


def mode(numbers):
    """Return the mode (most frequent number) of the list of numbers.
    If multiple values have the same highest frequency, return the smallest one.
    """
    if not numbers:
        raise ValueError("The list is empty.")

    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1

    max_freq = max(frequency.values())
    modes = [num for num, freq in frequency.items() if freq == max_freq]

    return min(modes)  # Return the smallest mode if multiple


# Example usage:
if __name__ == "__main__":
    sample_data = [4, 1, 2, 2, 3, 5]

    print("Sample data:", sample_data)
    print("Mean:", mean(sample_data))
    print("Median:", median(sample_data))
    print("Mode:", mode(sample_data))
