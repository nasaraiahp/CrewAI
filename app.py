import os
from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Configuration (Best practice: Store sensitive information securely, e.g., environment variables)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Securely store uploads
ALLOWED_EXTENSIONS = {'xlsx'}

# Helper function to check file extensions (Security: Prevent uploads of malicious file types)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_data(filepath):  # Helper function to load data
    try:
        df = pd.read_excel(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None  # Or handle appropriately, e.g., load default data
    except Exception as e:  # Handle other potential errors during file processing
        print(f"Error loading file: {e}")
        return None



@app.route('/')
def dashboard():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'your_excel_file.xlsx') # Use a default file, expecting upload functionality later
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  # Create if it doesn't exist

    df = load_data(filepath)  # Call the helper function
    if df is None:
        return "Error loading data. Please check console for details.", 500 # Return error to user


    # Prepare chart data (Efficiency: Perform data processing once)
    charts_data = {
        "chart1": {
            "labels": df['Column1'].tolist(),
            "data": df['Column2'].tolist(),
            "title": "Bar Chart Example"
        },
        "chart2": {
            "labels": df['Column3'].tolist(),
            "data": df['Column4'].tolist(),
            "title": "Line Chart Example"
        },
        "chart3": {
            "labels": df['Column5'].unique().tolist(),
            "data": df.groupby('Column5')['Column6'].sum().tolist(),
            "title": "Pie Chart Example"
        }
    }


    return render_template('dashboard.html', charts_data=charts_data)


if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False for production