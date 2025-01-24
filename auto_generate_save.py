from typing import List, Union

def sum_and_average(numbers: List[Union[int, float]]) -> tuple[Union[int, float], float]:
    """
    Calculates the sum and average of a list of numbers.

    Args:
        numbers: A list of numbers (integers or floats).

    Returns:
        A tuple containing the sum and average of the numbers.
        Returns (0, 0.0) if the input list is empty.
        Raises TypeError if the input list contains non-numerical elements.
        Raises ValueError if the input is not a list.
    """
    if not isinstance(numbers, list):
        raise ValueError("Input must be a list.")

    if not numbers:
        return 0, 0.0  # Handle empty list case, ensure consistent float type for average

    total = sum(numbers)  # More efficient than manual loop and check
    average = total / len(numbers)
    return total, average