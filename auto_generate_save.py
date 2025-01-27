from typing import List, Tuple

def analyze_numbers(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Analyzes a list of numbers to find the maximum, minimum, and average.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the maximum, minimum, and average of the numbers.
        Raises ValueError if the input list is empty.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty.")

    max_number = max(numbers)
    min_number = min(numbers)
    average = sum(numbers) / len(numbers)

    return max_number, min_number, average