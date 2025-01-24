from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        The sum of the numbers in the input list.
        Raises TypeError if input is not a list.
        Raises ValueError if the input list is empty.
        Raises TypeError if the input list contains non-numeric values (handled by sum()).


    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    return sum(numbers)