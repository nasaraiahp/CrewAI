from typing import List, Union

def sum_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Calculates the sum of a list of numbers.

    Args:
        numbers: A list of numbers (int or float).

    Returns:
        The sum of the numbers in the input list.
        Returns 0 if the input list is empty.
        Raises TypeError if the input is not a list or if the list contains non-numeric elements.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    # More efficient sum calculation using the built-in sum() function.
    # The check for numeric types is done within sum() using a generator expression combined with the all() function. 
    # The generator checks that each number is an instance of int or float. This avoids manual iteration and TypeError raising within the loop.

    if all(isinstance(number, (int, float)) for number in numbers):
      return sum(numbers)
    else:
      raise TypeError("List elements must be numbers (int or float).")



# Example usage demonstrating the improved function:

try:
    print(sum_numbers([1, 2, 3, 4, 5]))  # Output: 15
    print(sum_numbers([1.5, 2.5, 3.0]))  # Output: 7.0
    print(sum_numbers([]))  # Output: 0

    print(sum_numbers("hello"))  # Raises TypeError
    print(sum_numbers([1, 2, "a"]))  # Raises TypeError

except TypeError as e:
    print(f"Error: {e}")