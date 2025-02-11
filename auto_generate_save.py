from flask import Flask, render_template, request
from typing import List

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sum_numbers():
    result = None
    if request.method == "POST":
        try:
            numbers_str = request.form.get("numbers")
            if not numbers_str:
                raise ValueError("Input cannot be empty.")
            
            numbers_list_str = numbers_str.split(",")
            numbers: List[float] = []
            for x in numbers_list_str:
                try:
                    numbers.append(float(x.strip()))
                except ValueError:
                    raise ValueError(f"Invalid input: '{x.strip()}'. Please enter numbers separated by commas.")

            result = sum(numbers)

        except ValueError as e:
             result = f"Error: {e}"
        # Avoid catching generic exceptions. Be specific. If needed, catch Exception
        # only for logging purposes and re-raise.
        # except Exception as e:
        #     result = f"An unexpected error occurred: {str(e)}"  # Log the error for debugging

    return render_template("sum.html", result=result)

if __name__ == "__main__":
    app.run(debug=False) # Disable debug mode in production