from typing import List, Tuple

def min_max_sum(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Calculates the minimum, maximum, and sum of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the minimum, maximum, and sum of the numbers.
        Raises ValueError if the input list is empty.
        Raises TypeError if the input list contains non-numerical elements.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("Input list must contain only numbers.")

    min_val = min(numbers)
    max_val = max(numbers)
    total_sum = sum(numbers)

    return min_val, max_val, total_sum