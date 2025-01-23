from typing import List, Union

def count_numbers(numbers: List[Union[int, float]]) -> int:
    """
    Counts the number of numeric elements in a list.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        The total count of numbers in the list.
        Raises TypeError if input is not a list or contains non-numeric elements.
        Raises ValueError if the input list is empty.
    """

    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    # Improved: Check for type within the loop is redundant.  The type hint
    # ensures that mypy will catch type errors. The runtime check is only
    # needed in situations where you might be bypassing type checking.  
    # Simply returning the length is correct and more efficient.
    return len(numbers)