from flask import Flask, render_template, request
from typing import List, Union

app = Flask(__name__)

def calculate_average(numbers: List[Union[int, float]]) -> float:
    """Calculates the average of a list of numbers."""
    if not numbers:
        return 0  # Or raise a more specific exception like ValueError("Input list cannot be empty")
    return sum(numbers) / len(numbers)

@app.route("/", methods=["GET", "POST"])
def index():
    """Handles the main route for the application."""
    average = None
    error_message = None # Initialize error message
    if request.method == "POST":
        try:
            numbers_str = request.form.get("numbers")
            if not numbers_str:
                raise ValueError("Input cannot be empty") # Handle empty input
            numbers = [float(x.strip()) for x in numbers_str.split(",")] # Strip whitespace from each number
            average = calculate_average(numbers)
        except ValueError as e:
            error_message = "Invalid input. Please enter numbers separated by commas. " + str(e) # More informative error message
    return render_template("index.html", average=average, error=error_message) # Pass error message to template


if __name__ == "__main__":
    app.run(debug=False) # Disable debug mode in production