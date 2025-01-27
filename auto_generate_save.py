from typing import List, Tuple
import statistics  # More efficient for basic stats

def analyze_numbers(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Calculates the sum, maximum, and minimum of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the sum, maximum, and minimum of the numbers.
        Raises TypeError if input is not a list of numbers.
        Raises ValueError if the input list is empty or contains non-numeric values.
    """

    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")
    if not numbers:
        raise ValueError("Input list cannot be empty.")
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("Input list must contain only numbers.")


    # Use statistics module for potential performance gains with large lists
    total = sum(numbers) #statistics.fsum(numbers) if only floats are expected.
    maximum = max(numbers)
    minimum = min(numbers)

    return total, maximum, minimum


# Example Usage
try:
    numbers1 = [1.5, 2.7, 3.9, 4.2, 5.1]
    sum_result1, max_result1, min_result1 = analyze_numbers(numbers1)
    print(f"For {numbers1}: Sum={sum_result1}, Max={max_result1}, Min={min_result1}")

    numbers2 = []
    sum_result2, max_result2, min_result2 = analyze_numbers(numbers2)  # This will raise a ValueError
    print(f"For {numbers2}: Sum={sum_result2}, Max={max_result2}, Min={min_result2}")

    numbers3 = [1, 2, 'a']  # Example with incorrect type
    sum_result3, max_result3, min_result3 = analyze_numbers(numbers3)  # This will raise a ValueError
    print(f"For {numbers3}: Sum={sum_result3}, Max={max_result3}, Min={min_result3}")

except (ValueError, TypeError) as e:
    print(e)