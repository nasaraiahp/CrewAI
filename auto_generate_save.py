from typing import List, Union, Tuple

def list_stats(numbers: List[Union[int, float]]) -> Tuple[Union[int, float], Union[int, float], Union[int, float]]:
    """
    Calculates the sum, maximum, and minimum of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        A tuple containing the sum, maximum, and minimum values.
        Returns (0, 0, 0) if the input list is empty.

    Raises:
        TypeError: If input is not a list or contains non-numeric values.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        return 0, 0, 0  # Handle empty list case

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers (int or float).")

    total = sum(numbers)
    maximum = max(numbers)
    minimum = min(numbers)

    return total, maximum, minimum