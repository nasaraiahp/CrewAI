from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers (integers or floats).

    Returns:
        The sum of the numbers in the list.  The return type will typically
        match the input type (e.g., all integers will return an integer sum),
        unless a float is present or overflow occurs, in which case a float
        will be returned. Returns 0 if the list is empty.

    Raises:
        TypeError: If any element in the list is not an int or a float.
    """
    if not numbers:
        return 0  # Return 0 for an empty list

    if not all(isinstance(number, (int, float)) for number in numbers):
        raise TypeError("List elements must be integers or floats.")
    
    return sum(numbers)