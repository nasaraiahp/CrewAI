from typing import List, Union

def calculate_average(numbers: List[Union[int, float]]) -> float:
    """
    Calculates the average of a list of numbers.

    Args:
        numbers: A list of numbers (integers or floats).

    Returns:
        The average of the numbers in the input list.
        Raises TypeError if input is not a list or if the list contains non-numeric elements.
        Raises ValueError if the input list is empty.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    # Improved: Check types and sum in one loop for efficiency
    total = 0
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError("List elements must be numbers (int or float).")
        total += num

    return total / len(numbers)