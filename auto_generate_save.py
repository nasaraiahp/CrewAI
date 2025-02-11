from flask import Flask, render_template, request
from typing import List, Union

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sum_numbers():
    if request.method == "POST":
        numbers_str = request.form.get("numbers")
        if not numbers_str:
            return render_template("index.html", error="Please enter numbers.")

        try:
            numbers: List[Union[int, float]] = [float(x.strip()) for x in numbers_str.split(",")]
            total: Union[int, float]] = sum(numbers)
            return render_template("index.html", total=total, numbers=numbers_str)
        except ValueError:
            return render_template("index.html", error="Invalid input. Please enter comma-separated numbers.")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False) # Disable debug mode in production