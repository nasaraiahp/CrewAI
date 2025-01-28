from typing import List, Union

def analyze_list(numbers: List[Union[int, float]]) -> tuple[float, float, float]:
    """
    Analyzes a list of numbers to find the maximum, minimum, and sum.

    Args:
        numbers: A list of int or float numbers.

    Returns:
        A tuple containing the maximum, minimum, and sum of the numbers.
        Raises TypeError if input is not a list of numbers.
        Raises ValueError if the input list is empty.

    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be int or float.")

    if not numbers:
        raise ValueError("List cannot be empty.")

    # More efficient approach using built-in functions
    max_num = max(numbers)
    min_num = min(numbers)
    total = sum(numbers)

    return max_num, min_num, total