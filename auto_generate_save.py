from typing import List, Tuple, Union

def analyze_numbers(numbers: List[Union[int, float]]) -> Tuple[float, float, float]:
    """
    Calculates the sum, maximum, and minimum of a list of numbers.

    Args:
        numbers: A list of int or float numbers.

    Returns:
        A tuple containing the sum, maximum, and minimum values.
        Raises TypeError if input is not a list of numbers.
        Raises ValueError if the input list is empty.

    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be int or float.")

    if not numbers:
        raise ValueError("List cannot be empty.")

    # More efficient to calculate min/max once during iteration
    total = 0
    minimum = float('inf')  # Initialize with positive infinity
    maximum = float('-inf') # Initialize with negative infinity

    for num in numbers:
        total += num
        minimum = min(minimum, num)
        maximum = max(maximum, num)


    return total, maximum, minimum