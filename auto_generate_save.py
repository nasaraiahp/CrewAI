from typing import List, Union, Sequence

def calculate_average(numbers: Sequence[Union[int, float]]) -> float:
    """
    Calculates the average of a sequence of numbers.

    Args:
        numbers: A sequence of numbers (integers or floats).

    Returns:
        The average of the numbers in the input sequence.
        Raises TypeError if input is not a sequence or contains non-numeric values.
        Raises ValueError if the input sequence is empty.
    """
    if not numbers:
        raise ValueError("Input sequence cannot be empty.")

    # Check if all elements are int or float using a generator expression within all() for efficiency.
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("Sequence elements must be numbers (int or float).")

    return sum(numbers) / len(numbers)