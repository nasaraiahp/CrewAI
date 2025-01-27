from typing import List
import numbers

def analyze_numbers(numbers: List[float]) -> tuple[float, float, float]:
    """
    Analyzes a list of numbers to find the sum, maximum, and minimum values.

    Args:
        numbers: A list of numbers (float or int).

    Returns:
        A tuple containing the sum, maximum, and minimum values.
        Raises TypeError if input is not a list or if the list contains non-numeric elements.
        Raises ValueError if the input list is empty.

    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    # More efficient and Pythonic check for numeric types using the numbers module
    if not all(isinstance(num, numbers.Number) for num in numbers):  # Use numbers.Number for broader numeric type checking
        raise TypeError("List elements must be numeric.")


    # More efficient approach for small to medium-sized lists
    total = 0
    minimum = float('inf')
    maximum = float('-inf')

    for num in numbers:
        total += num
        minimum = min(minimum, num)
        maximum = max(maximum, num)


    return total, maximum, minimum