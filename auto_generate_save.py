from typing import List, Union, Sequence

def calculate_average(numbers: Sequence[Union[int, float]]) -> float:
    """
    Calculates the average of a list of numbers.

    Args:
        numbers: A sequence of numbers (int or float).

    Returns:
        The average of the numbers.
        Raises TypeError if input is not a sequence or contains non-numeric values.
        Raises ValueError if the input sequence is empty.
    """
    if not isinstance(numbers, Sequence):
        raise TypeError("Input must be a sequence.")

    if not numbers:
        raise ValueError("Input sequence cannot be empty.")

    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError("Sequence elements must be numbers (int or float).")

    return sum(numbers) / len(numbers)