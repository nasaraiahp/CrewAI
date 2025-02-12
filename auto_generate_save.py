from flask import Flask, render_template, request, jsonify
import pandas as pd
import io
import json
import os

app = Flask(__name__)

# Secure way to generate secret key (do this only once and store securely)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    chart_data = None
    error_message = None  # Initialize error message
    if request.method == "POST":
        try:
            file = request.files["excel_file"]
            if file.filename == '':
                raise ValueError("No selected file")

            # Check allowed file extensions for better security
            allowed_extensions = {'xls', 'xlsx'}
            if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                raise ValueError("Invalid file type. Please upload an Excel file (.xls or .xlsx).")


            # Use a more robust way to handle different Excel formats
            try:
                df = pd.read_excel(file)
            except Exception as e:
                 raise ValueError("Error reading Excel file. Please ensure it's a valid format." + str(e))

            # Explicitly select columns for charting (more robust)
            try:  # Make the column selection safer
                x_column = request.form.get('x_column') or df.columns[0]  # Default to 1st if none selected
                y_column = request.form.get('y_column') or df.columns[1]
                chart_data = {
                    "labels": df[x_column].tolist(),  # x-axis
                    "data": df[y_column].tolist()     # y-axis
                }

            except IndexError as e:
                raise ValueError("The Excel file needs at least two columns for charting. " + str(e))
            except KeyError as e:
                raise ValueError(f"Selected columns ({x_column}, {y_column}) not found in the Excel file. " + str(e))




        except ValueError as e:
            error_message = str(e)
        except Exception as e: # Catch general exceptions like incorrect file format
            error_message = "An unexpected error occurred during file processing." + str(e)

    return render_template("index.html", chart_data=chart_data, error=error_message)



if __name__ == "__main__":
    app.run(debug=True)