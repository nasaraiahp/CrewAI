from typing import List
import math

def analyze_numbers(numbers: List[float]) -> tuple[float, float, float]:
    """
    Calculates the sum, maximum, and minimum of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the sum, maximum, and minimum values.
        Raises ValueError if the input list is empty or contains non-numerical elements.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty.")

    for item in numbers:
        if not isinstance(item, (int, float)):
            raise ValueError("Input list must contain only numbers.")

    total = math.fsum(numbers)  # Use fsum for potentially improved floating-point accuracy
    maximum = max(numbers)
    minimum = min(numbers)

    return total, maximum, minimum


# Example usage
try:
    my_numbers = [1.5, 2.7, 3.2, 4.8, 0.1]
    sum_result, max_result, min_result = analyze_numbers(my_numbers)
    print(f"Sum: {sum_result}")
    print(f"Maximum: {max_result}")
    print(f"Minimum: {min_result}")

    empty_list = []
    sum_result, max_result, min_result = analyze_numbers(empty_list)  # This will raise a ValueError
except ValueError as e:
    print(f"Error: {e}")


try:
    my_numbers_with_string = [1.2, 2, "hello"]
    sum_result, max_result, min_result = analyze_numbers(my_numbers_with_string)  # This will now raise a ValueError
except ValueError as e:
    print(f"An error occurred: {e}")