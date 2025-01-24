from typing import List, Union, Sequence

def calculate_average(numbers: Sequence[Union[int, float]]) -> float:
    """
    Calculates the average of a sequence of numbers.

    Args:
        numbers: A sequence of numbers (int or float).

    Returns:
        The average of the numbers in the sequence.
        Raises ValueError if the sequence is empty or contains non-numeric values.

    """
    if not numbers:
        raise ValueError("Cannot calculate the average of an empty sequence.")

    # Check all types at once using all() for efficiency
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("Sequence must contain only numbers (int or float).")

    return sum(numbers) / len(numbers)



# Example usage with more concise error handling
try:
    my_numbers = [1, 2, 3, 4, 5]
    average = calculate_average(my_numbers)
    print(f"The average is: {average}")

    empty_list = []
    average = calculate_average(empty_list)  # This will raise a ValueError

except (ValueError, TypeError) as e: # Catch both potential errors
    print(f"Error: {e}")


try:
    my_numbers_with_string = [1, 2, "a", 4, 5]  # Example with a string
    average = calculate_average(my_numbers_with_string) # This will raise a ValueError

except (ValueError, TypeError) as e: # Catch both potential errors
    print(f"Error: {e}")


try:
    not_a_list = 123 # Example with a non-sequence type. Now handled correctly
    average = calculate_average(not_a_list) # This will raise a TypeError (because sum will attempt to iterate which won't work for int)

except (ValueError, TypeError) as e: # Catch both potential errors
    print(f"Error: {e}")