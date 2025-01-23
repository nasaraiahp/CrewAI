from typing import List, Union, Sequence

def sum_numbers(numbers: Sequence[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a sequence of numbers.

    Args:
        numbers: A sequence of numbers (int or float).

    Returns:
        The sum of the numbers in the input sequence.
        Returns 0 if the input sequence is empty.
        Raises TypeError if the input is not a sequence or if the sequence contains non-numeric values.

    """
    if not isinstance(numbers, Sequence):
        raise TypeError("Input must be a sequence (list, tuple, etc.).")

    total: Union[int, float] = 0
    for number in numbers:
        if not isinstance(number, (int, float)):
            raise TypeError("Sequence elements must be numbers (int or float).")
        total += number

    return total


# Example usage:
try:
    print(sum_numbers([1, 2, 3, 4.5]))  # Output: 10.5
    print(sum_numbers([]))  # Output: 0
    print(sum_numbers((1, 2, 3))) # Output: 6
    print(sum_numbers([1, 2, 'a']))  # Raises TypeError
    print(sum_numbers("123"))  # Raises TypeError

except TypeError as e:
    print(f"Error: {e}")