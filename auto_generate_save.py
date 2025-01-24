from typing import List, Tuple, Union

def min_max_sum(numbers: List[Union[int, float]]) -> Tuple[Union[float, None], Union[float, None], Union[float, None]]:
    """
    Calculates the minimum, maximum, and sum of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the minimum, maximum, and sum of the numbers.
        Returns (None, None, None) if the input list is empty.

    Raises:
        TypeError: If input is not a list or if the list contains non-numeric values.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        return None, None, None  # Handle empty list case

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List must contain only numbers (int or float).")

    min_val = float('inf')
    max_val = float('-inf')
    total = 0

    for num in numbers:
        min_val = min(min_val, num)
        max_val = max(max_val, num)
        total += num

    return min_val, max_val, total


# Example usage:

try:
    result = min_max_sum([1, 2, 3, 4, 5])
    print(f"Min: {result[0]}, Max: {result[1]}, Sum: {result[2]}")  # Output: Min: 1, Max: 5, Sum: 15

    result = min_max_sum([])
    print(result) # Output: (None, None, None)

    result = min_max_sum([1, 2.5, 3, 4, 5])
    print(f"Min: {result[0]}, Max: {result[1]}, Sum: {result[2]}")  # Output: Min: 1, Max: 5, Sum: 15.5


    result = min_max_sum([1, 2, 'a', 4, 5])  # Example with a non-numeric value
    print(result)  # Raises TypeError

except TypeError as e:
    print(f"Error: {e}")