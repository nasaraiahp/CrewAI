from typing import List, Union

def sum_and_average(numbers: List[Union[int, float]]) -> tuple[Union[int, float], float]:
    """
    Calculates the sum and average of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        A tuple containing the sum and average of the numbers.
        Returns (0, 0.0) if the input list is empty.
        Raises TypeError if the input is not a list or contains non-numeric values.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        return 0, 0.0  # Handle empty list case

    # More efficient sum calculation using built-in sum()
    total = sum(numbers)

    # Check for numeric types after summing for efficiency
    if not all(isinstance(num, (int, float)) for num in numbers):  #check if all are numbers
        raise TypeError("List elements must be numbers (int or float).")


    average = total / len(numbers)
    return total, average