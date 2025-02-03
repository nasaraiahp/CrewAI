from typing import List, Tuple

def analyze_numbers(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Calculates the sum, minimum, and maximum of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the sum, minimum, and maximum of the numbers.
        Returns (0, 0, 0) if the input list is empty.
        Raises TypeError if input is not a list or if the list elements are not numbers.
       
    """

    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers.")

    if not numbers:
        return 0.0, 0.0, 0.0  # Return floats for consistency


    total = sum(numbers)
    minimum = min(numbers)
    maximum = max(numbers)

    return total, minimum, maximum