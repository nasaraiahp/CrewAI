from typing import List, Tuple, Union

def analyze_list(numbers: List[Union[int, float]]) -> Tuple[Union[int, float], Union[int, float], Union[int, float]]:
    """
    Analyzes a list of numbers to find the maximum, minimum, and sum.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        A tuple containing the maximum, minimum, and sum of the numbers.
        Raises TypeError if the input is not a list or if the list elements are not numbers.
        Raises ValueError if the input list is empty.
    """

    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers (int or float).")

    if not numbers:
        raise ValueError("Input list cannot be empty.")

    # More efficient approach using built-in functions
    max_num = max(numbers)
    min_num = min(numbers)
    total_sum = sum(numbers)

    return max_num, min_num, total_sum