from typing import List, Union, Tuple

def count_numbers(numbers: List[Union[int, float]]) -> Tuple[int, None]:
    """Counts the number of elements within a list of numbers.

    Args:
        numbers: A list of numerical values (integers or floats).

    Returns:
        The count of numbers in the list.
        Raises TypeError if the input is not a list.
        Raises ValueError if the list contains non-numeric values.

    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    count = 0
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise ValueError("List elements must be numbers.")
        count += 1
    return count

# Example usage
numbers1 = [1, 2, 3, 4, 5]
try:
    count1 = count_numbers(numbers1)
    print(f"Count of numbers in numbers1: {count1}")
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

numbers2 = [1, 2, "a", 4, 5]
try:
    count2 = count_numbers(numbers2)
    print(f"Count of numbers in numbers2: {count2}")
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

numbers3 = (1, 2, 3, 4, 5)
try:
    count3 = count_numbers(numbers3)
    print(f"Count of numbers in numbers3: {count3}")
except (TypeError, ValueError) as e:
    print(f"Error: {e}")