from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> float:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        The sum of the numbers in the list.
        Raises TypeError if the input is not a list or contains non-numeric values.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    total = 0.0  # Initialize total as a float for consistency
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError("List elements must be numbers (int or float).")
        total += num
    return total



# Example usage:
try:
    print(sum_numbers([1, 2, 3, 4, 5]))  # Output: 15.0
    print(sum_numbers([1.5, 2.5, 3.0]))  # Output: 7.0
    print(sum_numbers([]))  # Output: 0.0

    # Test cases that raise TypeError
    print(sum_numbers("hello"))  # Raises TypeError
    print(sum_numbers([1, 2, "a"])) # Raises TypeError

except TypeError as e:
    print(f"Error: {e}")