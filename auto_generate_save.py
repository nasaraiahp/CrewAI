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

            try:
                # More efficient parsing using list comprehension and map
                numbers_list: List[float] = [float(x.strip()) for x in numbers_str.split(',')]
                if not numbers_list:  # Check after conversion
                    raise ValueError("List of numbers cannot be empty.")

                result = sum(numbers_list) / len(numbers_list)
            except ValueError as e:
                # More specific error message for parsing issues
                result = f"Error: Invalid input. Please enter numbers separated by commas. ({e})"

        except ValueError as e:
            result = f"Error: {e}"  # Generic error handling
    return render_template("average.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)