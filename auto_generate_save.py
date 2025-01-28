from typing import List, Tuple

def min_max_avg(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Calculates the minimum, maximum, and average of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the minimum, maximum, and average of the numbers.
        Returns (None, None, None) if the list is empty.

    Raises:
        TypeError: If input is not a list or if the list contains non-numeric values.
        ValueError: If the input list is empty.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        return None, None, None  # Return None for empty list as documented

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numeric.")

    min_val = numbers[0]  # Initialize with the first element for efficiency
    max_val = numbers[0]
    total = 0

    for number in numbers:
        min_val = min(min_val, number)
        max_val = max(max_val, number)
        total += number

    avg = total / len(numbers)

    return min_val, max_val, avg