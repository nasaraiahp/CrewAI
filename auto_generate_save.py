from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        The sum of the numbers in the input list.
        Returns 0 if the list is empty.
        Raises TypeError if any element in the list is not an int or float.
    """
    if not numbers:
        return 0  # Handle empty list case

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers (int or float)")
    
    return sum(numbers)



# Example usage:
try:
    print(sum_numbers([1, 2, 3, 4.5]))  # Output: 10.5
    print(sum_numbers([]))  # Output: 0
    print(sum_numbers([1, 2, 'a']))  # Raises TypeError
except TypeError as e:
    print(f"Error: {e}")