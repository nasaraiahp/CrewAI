from typing import List, Tuple

def analyze_numbers(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Analyzes a list of numbers to find the sum, maximum, and minimum values.

    Args:
        numbers: A list of numbers (float or int).

    Returns:
        A tuple containing the sum, maximum, and minimum values.
        Raises TypeError if input is not a list or contains non-numeric values.
        Raises ValueError if the input list is empty.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers (int or float).")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    # Optimization: Use a single loop to calculate sum, max, and min
    total = 0.0
    maximum = float('-inf')  # Initialize with negative infinity
    minimum = float('inf')  # Initialize with positive infinity

    for num in numbers:
        total += num
        maximum = max(maximum, num)
        minimum = min(minimum, num)

    return total, maximum, minimum



# Example usage:
try:
    my_numbers = [1.5, 2, 3.7, 4, 5.1]
    sum_result, max_result, min_result = analyze_numbers(my_numbers)
    print(f"Sum: {sum_result}")
    print(f"Maximum: {max_result}")
    print(f"Minimum: {min_result}")

    empty_list = []
    sum_result, max_result, min_result = analyze_numbers(empty_list)  # This will raise a ValueError
except (TypeError, ValueError) as e:
    print(f"Error: {e}")


try:
    invalid_list = [1, 2, 'a']
    sum_result, max_result, min_result = analyze_numbers(invalid_list) # This will raise a TypeError
except (TypeError, ValueError) as e:
    print(f"Error: {e}")