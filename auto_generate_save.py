from flask import Flask, render_template, request
import pandas as pd
import os
import json

app = Flask(__name__)

# Configuration (better to store sensitive information outside the codebase, e.g., in environment variables)
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
UPLOAD_FOLDER = 'uploads'  # Create this folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit

# Helper function to check file extensions (security)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_charts(filepath):
    """Reads Excel data and creates chart data."""
    try:
        df = pd.read_excel(filepath)
        charts = []

        for i in range(min(10, len(df.columns))):
            try:
                chart_data = {
                    "labels": df.index.tolist(),
                    "datasets": [
                        {
                            "label": df.columns[i],
                            "data": df.iloc[:, i].tolist(),
                        }
                    ]
                }
                charts.append(json.dumps(chart_data))
            except (KeyError, IndexError, TypeError) as e:  # Include TypeError
                print(f"Error creating chart {i+1}: {e}")
                charts.append(json.dumps({"error": f"Could not create chart {i+1}: {e}"})) # More specific error message

        return charts

    except FileNotFoundError:
        print(f"Error: Excel file '{filepath}' not found.")
        return None
    except pd.errors.ParserError: # Handle corrupt Excel files
        print(f"Error: Could not parse Excel file '{filepath}'. File may be corrupt.")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


@app.route("/", methods=['GET', 'POST'])
def dashboard():
    charts_data = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template("dashboard.html", error="No file part")  # Provide error messages to user

        file = request.files['file']
        if file.filename == '':
            return render_template("dashboard.html", error="No selected file")

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)  # Secure way to save files
            file.save(filename)                                           # Use os.path.join
            charts_data = create_charts(filename)



    return render_template("dashboard.html", charts=charts_data)



if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) # Ensures upload directory exists
    app.run(debug=True)  # Never run with debug=True in production