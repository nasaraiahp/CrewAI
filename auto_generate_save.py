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
                result = "Input is required."  # Handle empty input
            else:
                numbers_list: List[Union[int, float]] = [
                    float(x.strip()) for x in numbers_str.split(",") if x.strip()
                ]
                if numbers_list:
                    result = sum(numbers_list) / len(numbers_list)
                else:
                    result = "Invalid input. Please enter numbers separated by commas." # Clarify error message for empty list after stripping


        except ValueError:
            result = "Invalid input. Please enter valid numbers separated by commas." # More specific error message
    return render_template("average.html", result=result)


if __name__ == "__main__":
    app.run(debug=False) # Disable debug in production