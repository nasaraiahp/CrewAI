from typing import List, Union, Sequence

def sum_numbers(numbers: Sequence[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A sequence of numbers (int or float).

    Returns:
        The sum of the numbers in the input sequence.
        Returns 0 if the input sequence is empty.
        Raises TypeError if the input is not a sequence or contains non-numeric elements.
    """
    if not isinstance(numbers, Sequence):
        raise TypeError("Input must be a sequence.")

    total = 0
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError("Sequence elements must be numbers (int or float).")
        total += num
    return total



# Example usage:
try:
    print(sum_numbers([1, 2, 3, 4, 5]))  # Output: 15
    print(sum_numbers([1.5, 2.5, 3.0])) # Output: 7.0
    print(sum_numbers([])) # Output: 0
    print(sum_numbers((1, 2, 3)))  # Now works with tuples as well!
    print(sum_numbers([1, 2, 'a']))  # Raises TypeError
    print(sum_numbers("123")) # Raises TypeError

except TypeError as e:
    print(f"Error: {e}")