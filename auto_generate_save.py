from typing import List, Union

def analyze_numbers(numbers: List[Union[int, float]]) -> tuple[float, float, float]:
    """
    Calculates the sum, maximum, and minimum of a list of numbers.

    Args:
        numbers: A list of int or float numbers.

    Returns:
        A tuple containing the sum, maximum, and minimum values.
        Raises TypeError if input is not a list or if the list contains non-numeric values.
        Raises ValueError if the input list is empty.

    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers (int or float).")

    total = sum(numbers)
    maximum = max(numbers)
    minimum = min(numbers)

    return total, maximum, minimum


# Example usage demonstrating both success and error handling
test_cases = [
    ([1.5, 2, 3.7, 4, 5.2], "Valid input"),
    ([], "Empty list"),
    ([1, 2, 'a', 4, 5], "List with a non-numeric element"),
    ("hello", "Not a list"),  # Include a non-list input for testing
    ([1, 2.5, 3, 4.0, 5], "Valid integers and floats"), # Example with mixed ints and floats
]

for input_data, case_description in test_cases:
    print(f"\nTesting: {case_description}")
    try:
        sum_result, max_result, min_result = analyze_numbers(input_data)
        print("Sum:", sum_result)
        print("Maximum:", max_result)
        print("Minimum:", min_result)
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")