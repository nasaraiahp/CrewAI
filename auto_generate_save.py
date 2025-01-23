from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        The sum of the numbers in the list.

    Raises:
        TypeError: If the input is not a list or contains non-numeric elements.
        ValueError: If the input list is empty.
    """

    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    if not all(isinstance(num, (int, float)) for num in numbers):  # More efficient check
        raise TypeError("List elements must be numbers (int or float).")

    total = sum(numbers)
    return total