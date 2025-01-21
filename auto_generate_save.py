from decimal import Decimal
from typing import List, Union

def sum_numbers(numbers: List[Union[int, float, Decimal]]) -> Union[int, float, Decimal]:
    """
    Sums a list of numbers (int, float, or Decimal).

    Args:
        numbers: A list of numbers.

    Returns:
        The sum of the numbers.  The return type is int if all inputs are int,
        float if any input is float, and Decimal if any input is Decimal and
        no inputs are float.

    Raises:
        TypeError: If input is not a list, or if any element in the list
            is not an int, float, or Decimal.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    has_float = False
    has_decimal = False

    for number in numbers:
        if not isinstance(number, (int, float, Decimal)):
            raise TypeError(f"Invalid type for list element: {type(number)}")
        if isinstance(number, float):
            has_float = True
        elif isinstance(number, Decimal):
            has_decimal = True

    if has_float:
        result = float(0)
    elif has_decimal:
        result = Decimal(0)
    else:
        result = 0

    for number in numbers:
        result += number

    return result