from typing import List, Tuple

def analyze_numbers(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Analyzes a list of numbers to find the maximum, minimum, and sum.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the maximum, minimum, and sum of the numbers.

    Raises:
        ValueError: If the input list is empty or contains non-numeric values.
        TypeError: If the input is not a list.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("Input list must contain only numbers.")

    # More efficient approach using built-in functions
    max_num = max(numbers)
    min_num = min(numbers)
    total = sum(numbers)

    return max_num, min_num, total


# Example usage:

try:
    result = analyze_numbers([1.5, 2.7, 3, 4.2, 5])
    print(f"Maximum: {result[0]}, Minimum: {result[1]}, Sum: {result[2]}")

    result = analyze_numbers([])  # Test empty list
except ValueError as e:
    print(f"Error: {e}")

try:
    result = analyze_numbers([1, 2, 'a'])  # Test invalid input
except ValueError as e:
    print(f"Error: {e}")


try:
    result = analyze_numbers("not a list")
except TypeError as e:
    print(f"Error: {e}")