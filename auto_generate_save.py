from typing import List, Tuple

def analyze_numbers(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Analyzes a list of numbers to calculate the sum, maximum, and minimum values.

    Args:
        numbers: A list of numbers (float or int).

    Returns:
        A tuple containing the sum, maximum, and minimum values.
        Raises ValueError if the input list is empty or contains non-numeric values.
        Raises TypeError if the input is not a list.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    try:
        total = sum(numbers)
        maximum = max(numbers)
        minimum = min(numbers)
    except TypeError as e:
        raise TypeError("List elements must be numbers.") from e  # Chain the exception
    except ValueError as e: # this catches empty list from min/max
        raise ValueError("List elements must be numbers.") from e

    return total, maximum, minimum



# Example usage:

try:
    result = analyze_numbers([1, 2, 3, 4, 5])
    print(f"Sum: {result[0]}, Max: {result[1]}, Min: {result[2]}")

    result = analyze_numbers([1.5, 2.5, 3, 4, 5])  # Handles floats as well
    print(f"Sum: {result[0]}, Max: {result[1]}, Min: {result[2]}")

    result = analyze_numbers([]) # Now correctly raises ValueError
    print(f"Sum: {result[0]}, Max: {result[1]}, Min: {result[2]}") 

    result = analyze_numbers([1, 2, "a"])  # Demonstrates type error handling
except (TypeError, ValueError) as e:
    print(f"Error: {e}")