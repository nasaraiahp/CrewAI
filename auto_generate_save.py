from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        The sum of the numbers in the input list.
        Returns 0 if the input list is empty.
        Raises TypeError if input is not a list or if the list contains non-numeric values.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    total: float = 0  # Initialize to float for consistency
    for number in numbers:
        if not isinstance(number, (int, float)):
            raise TypeError("List elements must be numbers (int or float).")
        total += number

    return total