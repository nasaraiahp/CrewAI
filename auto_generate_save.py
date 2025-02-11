from flask import Flask, render_template, request
from typing import List, Union

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def average():
    result = None
    if request.method == "POST":
        try:
            numbers_str = request.form.get("numbers")
            if not numbers_str:
                raise ValueError("Input cannot be empty.")

            # Improved number parsing with more robust error handling
            try:
                numbers_list = [float(x.strip()) for x in numbers_str.split(",")]
                numbers_list = [x for x in numbers_list if x is not None]  # Remove any None values
            except ValueError:
                raise ValueError("Invalid input. Please enter numbers separated by commas.")


            if not numbers_list:
                raise ValueError("Please enter valid numbers.")

            result = sum(numbers_list) / len(numbers_list)
        except ValueError as e:
            result = f"Error: {e}"
        except Exception as e:  # Catching general exceptions for robustness.  Log this!
            result = "An unexpected error occurred. Please try again later."  # Don't expose internal error details
            print(f"Unexpected error: {e}") # Log the actual error for debugging

    return render_template("average.html", result=result)


if __name__ == "__main__":
    app.run(debug=False) # Disable debug mode in production