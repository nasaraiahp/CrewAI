from typing import List, Tuple

def min_max_sum(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Calculates the minimum, maximum, and sum of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the minimum, maximum, and sum of the numbers.
        Returns (0, 0, 0) if the input list is empty.
    Raises:
        TypeError: If input is not a list or if the list elements are not numbers.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers.")

    if not numbers:
        return 0.0, 0.0, 0.0  # Return float zeros for consistency

    # More efficient approach using built-in functions
    min_num = min(numbers)
    max_num = max(numbers)
    total_sum = sum(numbers)

    return min_num, max_num, total_sum