from typing import List, Tuple, Union

def list_stats(numbers: List[Union[int, float]]) -> Tuple[float, float, float]:
    """
    Calculates the maximum, minimum, and average of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        A tuple containing the maximum, minimum, and average of the numbers.
        Returns (0, 0, 0) if the list is empty.

    Raises:
        TypeError: If input is not a list or contains non-numeric values.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be int or float.")

    if not numbers:
        return 0.0, 0.0, 0.0  # Handle empty list case

    max_num = max(numbers)
    min_num = min(numbers)
    average = sum(numbers) / len(numbers)

    return max_num, min_num, average