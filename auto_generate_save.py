from typing import List, Tuple

def summarize_numbers(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Calculates the sum, maximum, and minimum of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the sum, maximum, and minimum of the numbers.
        Returns (0.0, 0.0, 0.0) if the input list is empty.

    Raises:
        TypeError: If input is not a list or contains non-numeric values.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        return 0.0, 0.0, 0.0  # Handle empty list case

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers.")

    # More efficient to calculate min/max once, not via separate function calls.
    minimum = maximum = numbers[0]
    total = 0.0 # Initialize total to float for consistency

    for num in numbers:  # Iterate once to calculate sum, min, max
        total += num
        if num < minimum:
            minimum = num
        elif num > maximum:
            maximum = num
            
    return total, maximum, minimum


# Example usage
try:
    my_numbers = [1.5, 2.0, 3.7, 4, 5.2]
    sum_result, max_result, min_result = summarize_numbers(my_numbers)
    print(f"Sum: {sum_result}, Max: {max_result}, Min: {min_result}")

    empty_list = []
    sum_result, max_result, min_result = summarize_numbers(empty_list)
    print(f"Sum: {sum_result}, Max: {max_result}, Min: {min_result}")

    invalid_list = [1, 2, 'a', 4]
    sum_result, max_result, min_result = summarize_numbers(invalid_list)
    print(f"Sum: {sum_result}, Max: {max_result}, Min: {min_result}")


except TypeError as e:
    print(f"Error: {e}")

except Exception as e:  # Catching any other potential errors
    print(f"An unexpected error occurred: {e}")