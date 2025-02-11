from typing import List, Tuple
from flask import Flask, render_template, request

app = Flask(__name__)

def min_max_sum(numbers: List[float]) -> Tuple[float, float, float]:
    """
    Calculates the minimum, maximum, and sum of a list of numbers.

    Args:
        numbers: A list of numbers.

    Returns:
        A tuple containing the minimum, maximum, and sum of the numbers.
        Returns (None, None, None) if the input list is empty.
        Raises TypeError if the input list contains non-numeric values.
    """
    if not numbers:
        return None, None, None

    try:
        min_val = min(numbers)
        max_val = max(numbers)
        sum_val = sum(numbers)
        return min_val, max_val, sum_val
    except TypeError as e:
        raise TypeError("List elements must be numeric.") from e  # More descriptive error message


@app.route("/", methods=["GET", "POST"])
def index():
    min_val = None
    max_val = None
    sum_val = None
    avg_val = None
    error_msg = None  # Initialize error_msg

    if request.method == "POST":
        try:
            numbers_str = request.form.get("numbers")
            if not numbers_str:
                 raise ValueError("Input cannot be empty.") # Handle empty input case.
            numbers = [float(x.strip()) for x in numbers_str.split(",")] # strip whitespace from input
            min_val, max_val, sum_val = min_max_sum(numbers)
            if sum_val is not None:
                avg_val = sum_val / len(numbers)
        except (ValueError, TypeError) as e:
            error_msg = str(e)  # Store the specific error message

    return render_template("index.html", min=min_val, max=max_val, sum=sum_val, avg=avg_val, error=error_msg)


if __name__ == "__main__":
    app.run(debug=True)