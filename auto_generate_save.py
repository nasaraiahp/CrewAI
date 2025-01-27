from typing import List, Union, Tuple

def min_max_sum(numbers: List[Union[int, float]]) -> Tuple[Union[float, None], Union[float, None], Union[float, None]]:
    """
    Calculates the minimum, maximum, and sum of a list of numbers.

    Args:
        numbers: A list of numbers (float or int).

    Returns:
        A tuple containing the minimum, maximum, and sum of the numbers.
        Returns (None, None, None) if the input is not a list, 
        contains non-numeric values, or is empty.
    """
    if not isinstance(numbers, list):
        return None, None, None  # Or log the error

    if not all(isinstance(num, (int, float)) for num in numbers):
        return None, None, None # Or log the error

    if not numbers:
        return None, None, None # Or log the error
    
    min_val = min(numbers)
    max_val = max(numbers)
    total = sum(numbers)

    return min_val, max_val, total