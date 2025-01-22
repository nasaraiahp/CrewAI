from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> float:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers to sum.

    Returns:
        The sum of the numbers in the input list.
        Raises TypeError if input is not a list or contains non-numeric values.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    total: float = 0
    for number in numbers:
        if not isinstance(number, (int, float)):
            raise TypeError("List elements must be numbers.")
        total += number
    return total