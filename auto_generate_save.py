from typing import List, Union

def list_stats(numbers: List[Union[int, float]]) -> tuple[float, float, float]:
    """
    Calculates the sum, minimum, and maximum of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        A tuple containing the sum, minimum, and maximum of the numbers.
        Raises TypeError if the list contains non-numeric values.
        Raises ValueError if the input list is empty.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List must contain only numbers (int or float).")

    total = 0
    minimum = float('inf')  # Initialize with positive infinity
    maximum = float('-inf') # Initialize with negative infinity

    for num in numbers:
        total += num
        minimum = min(minimum, num)
        maximum = max(maximum, num)

    return total, minimum, maximum