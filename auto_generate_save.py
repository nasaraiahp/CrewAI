from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> float:
    """Calculates the sum of a list of numbers.

    Args:
        numbers: A list of integers or floats.

    Returns:
        The sum of the numbers in the list. Returns 0.0 if the list is empty.

    Raises:
        TypeError: If the list contains non-numeric elements.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        return 0.0

    total = 0.0
    for i, number in enumerate(numbers):
        if isinstance(number, (int, float)):
            total += number
        else:
            raise TypeError(f"Element at index {i} is of type {type(number)}, but must be a number.")

    return total