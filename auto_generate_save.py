from typing import List, Union

def list_analysis(numbers: List[Union[int, float]]) -> tuple[float, float, float]:
    """
    Calculates the sum, maximum, and minimum of a list of numbers.

    Args:
        numbers: A list of numbers (float or int).

    Returns:
        A tuple containing the sum, maximum, and minimum of the list.
        Returns (0.0, 0.0, 0.0) if the list is empty.  Type consistency maintained.
        Raises TypeError if input is not a list or if the list contains non-numeric values.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        return 0.0, 0.0, 0.0  # Handle empty list case, ensuring float return type

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numeric.")

    # More efficient approach for small to medium sized lists
    list_sum = 0.0
    maximum = float('-inf')  # Initialize with negative infinity for correct max calculation
    minimum = float('inf')    # Initialize with positive infinity for correct min calculation

    for num in numbers:
        list_sum += num
        maximum = max(maximum, num)
        minimum = min(minimum, num)

    return list_sum, maximum, minimum