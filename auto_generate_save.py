from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        The sum of the numbers in the list.
        Returns 0 if the list is empty.

    Raises:
        TypeError: If any element in the list is not an int or float.
    """
    if not numbers:
        return 0  # Handle empty list case

    total = 0
    for number in numbers:
        if not isinstance(number, (int, float)):
            raise TypeError("List elements must be numbers (int or float)")
        total += number
    return total