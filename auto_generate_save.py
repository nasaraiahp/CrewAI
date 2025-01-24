from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers (integers or floats).

    Returns:
        The sum of the numbers in the list.
        Returns 0 if the list is empty.
        Raises TypeError if input is not a list or if the list contains non-numeric elements.

    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:
        return 0  # Handle empty list case

    # More efficient sum calculation using built-in sum()
    total = sum(numbers)

    # Check for numeric after summing for efficiency
     if not all(isinstance(number, (int, float)) for number in numbers) :
        raise TypeError("List elements must be numbers (int or float).")
    
    return total