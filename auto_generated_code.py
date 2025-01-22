
def sum_numbers(numbers: list[int]) -> int:
    """Return the sum of a list of numbers with type hints and error handling."""
    if not isinstance(numbers, list) or not all(isinstance(n, (int, float)) for n in numbers):
        raise TypeError("Input must be a list of numbers.")
    return sum(numbers)
