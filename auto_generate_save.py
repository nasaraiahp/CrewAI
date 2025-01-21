from typing import List, Union, Sequence

def sum_numbers(numbers: Sequence[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list or tuple of numbers.

    Args:
        numbers: A sequence of numbers (int or float).

    Returns:
        The sum of the numbers in the sequence.
        Returns 0 if the input sequence is empty.

    Raises:
        TypeError: If the sequence contains non-numeric elements.
    """

    total = 0
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError("Sequence elements must be numbers (int or float).")
        total += num
    return total


# Example usage:
try:
    print(sum_numbers([1, 2, 3, 4.5]))  # Output: 10.5
    print(sum_numbers([]))  # Output: 0
    print(sum_numbers((1, 2, 3)))  # Output: 6  Example with tuple
    print(sum_numbers([1, 2, 'a']))  # Raises TypeError
except TypeError as e:
    print(f"Error: {e}")


try:
    print(sum_numbers("not a list")) # Raises TypeError
except TypeError as e:
    print(f"Error: {e}")