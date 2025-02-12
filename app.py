import os

import pandas as pd
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Configuration (Best practice to separate configuration)
app.config['EXCEL_FILE'] = 'data.xlsx'  # Relative path
app.config['UPLOAD_FOLDER'] = 'uploads'  # For future file uploads
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}  # Allowed file types

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])  # Handle POST for potential file uploads
def dashboard():
    if request.method == 'POST':  # Handle file upload (Future enhancement)
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Use secure filenames
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Process the uploaded file (e.g., update EXCEL_FILE path)
            # ...

    # Try to read Excel file, handle exceptions gracefully
    try:
        excel_file = app.config.get('EXCEL_FILE')
        if not os.path.exists(excel_file):
            raise FileNotFoundError(f"Excel file not found: {excel_file}")

        df = pd.read_excel(excel_file)

        # Prepare chart data (use a helper function for clarity)
        chart_data = prepare_chart_data(df)

        return render_template('dashboard.html', chart_data=chart_data)

    except FileNotFoundError as e:
        return render_template('error.html', error_message=str(e))  # Dedicated error page
    except (pd.errors.ParserError, KeyError) as e: # Catch specific Excel read errors
        return render_template('error.html', error_message=f"Error processing Excel file: {e}")  # More informative error message
    except Exception as e:
        # Log unexpected errors for debugging (Important for security and maintenance)
        app.logger.exception("An unexpected error occurred") # Use Flask's logger
        return render_template('error.html', error_message="An unexpected error occurred. Please check logs.")  # Generic message to users


def prepare_chart_data(df):
    """Helper function to prepare chart data from DataFrame."""
    try:
        return {
            'chart1': {'labels': df['Category'].tolist(), 'data': df['Value'].tolist()},
            'chart2': {'labels': df['Date'].dt.strftime('%Y-%m-%d').tolist(), 'data': df['Sales'].tolist()},
            'chart3': {'labels': df['Product'].tolist(), 'values': df['Quantity'].tolist()},
        }
    except KeyError as e:
        raise KeyError(f"Missing column in Excel file: {e}") # Re-raise exception for handling by caller



if __name__ == '__main__':
    app.run(debug=True) # Never set debug=True in production