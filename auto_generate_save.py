from typing import List, Union, Sequence

def sum_numbers(numbers: Sequence[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A sequence of numbers (int or float).

    Returns:
        The sum of the numbers in the sequence.
        Returns 0 if the input sequence is empty.
        Raises TypeError if input is not a sequence or contains non-numeric values.

    """
    if not isinstance(numbers, Sequence):
        raise TypeError("Input must be a sequence.")

    total: Union[int, float] = 0
    for number in numbers:
        if not isinstance(number, (int, float)):
            raise TypeError("Sequence elements must be numbers (int or float).")
        total += number
    return total