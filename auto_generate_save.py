from typing import List, Union

def calculate_average(numbers: List[Union[int, float]]) -> float:
    """
    Calculates the average of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        The average of the numbers in the list.

    Raises:
        TypeError: If the input is not a list or contains non-numeric values.
        ValueError: If the input list is empty.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    # More efficient way to check types and calculate the sum in one loop.  The previous version iterated twice unnecessarily
    total = 0
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError("List elements must be numbers (int or float).")
        total += num  

    return total / len(numbers)