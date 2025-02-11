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

            # More efficient string splitting and number conversion
            try:
                numbers: List[float] = [float(x) for x in numbers_str.split(",") if x.strip()]
            except ValueError:
                raise ValueError("Invalid input: Please enter numbers separated by commas.")

            if not numbers:
                raise ValueError("Please provide at least one number.")

            average_val = sum(numbers) / len(numbers)
            result = f"The average is: {average_val}"

        except ValueError as e:
            result = f"Error: {e}"

    return render_template("average.html", result=result)

if __name__ == "__main__":
    app.run(debug=False)  # Disable debug mode in production