from typing import List, Tuple, Union

def calculate_stats(numbers: List[Union[int, float]]) -> Tuple[Union[float, None], Union[float, None], Union[float, None]]:
    """
    Calculates the maximum, minimum, and average of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the maximum, minimum, and average of the numbers.
        Returns (None, None, None) if the input list is empty.

    Raises:
        TypeError: If the input is not a list or contains non-numerical elements.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    if not numbers:  # Handle empty list case
        return None, None, None

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers.")

    # More efficient approach using built-in functions for min, max, and sum
    max_num = max(numbers)
    min_num = min(numbers)
    total = sum(numbers)
    average = total / len(numbers)

    return max_num, min_num, average


# Example usage:
try:
    my_numbers = [1, 2, 3, 4, 5]
    maximum, minimum, average = calculate_stats(my_numbers)
    if maximum is not None: # handles empty list case gracefully
        print("Maximum:", maximum)
        print("Minimum:", minimum)
        print("Average:", average)

    empty_list = []
    maximum, minimum, average = calculate_stats(empty_list)
    if maximum is None:
        print("The list is empty.")


    invalid_list = [1, 2, 'a', 4, 5]
    maximum, minimum, average = calculate_stats(invalid_list)  # This will raise a TypeError

except TypeError as e:
    print("Error:", e)