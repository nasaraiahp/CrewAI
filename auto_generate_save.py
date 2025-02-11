from flask import Flask, render_template, request
from typing import List

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sum_numbers():
    result = None
    error_message = None  # Initialize error_message

    if request.method == "POST":
        numbers_str = request.form.get("numbers")
        if not numbers_str:
            error_message = "Input cannot be empty."
        else:
            try:
                numbers_list = [float(num_str.strip()) for num_str in numbers_str.split(',')]
                result = sum(numbers_list)
            except ValueError as e:
                error_message = f"Invalid input: {e}" # More informative error message

    return render_template("index.html", result=result, error=error_message) # Pass error to template


if __name__ == "__main__":
    app.run(debug=False) # Disable debug in production