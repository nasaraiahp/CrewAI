from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import json
import werkzeug

app = Flask(__name__)

# Secure way to generate secret key (Do this ONLY ONCE and store it securely)
# import secrets
# app.secret_key = secrets.token_hex(16)  # Store this securely!
app.secret_key = os.environ.get("SECRET_KEY") or "your-secret-key"  # for now


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_chart_data(df):
    """Generates chart data from the DataFrame."""
    try:
        # More flexible chart data generation:
        chart_type = request.form.get('chart_type', 'bar')  # Default to bar chart
        x_axis = request.form.get('x_axis') # No default value, it is mandatory
        y_axis = request.form.get('y_axis') #No default value, it is mandatory

        if not x_axis or not y_axis:
            return jsonify({'error': "X-axis and Y-axis must be selected."})


        if chart_type in ['bar', 'line']: #only sum aggregation supported for simplicity for now
            grouped_data = df.groupby(x_axis)[y_axis].sum().reset_index()
        else:  #other chart types not implemented for now
             return jsonify({'error': f"Chart type {chart_type} not yet supported"})

        labels = grouped_data[x_axis].tolist()
        data = grouped_data[y_axis].tolist()
        return jsonify({'labels': labels, 'data': data, 'chart_type': chart_type})


    except KeyError as e:
        return jsonify({'error': f"Column not found: {e}"})
    except Exception as e:
        app.logger.error(f"Error creating chart data: {e}")  # Log the error
        return jsonify({'error': "An unexpected error occurred."}) # do not return raw error


@app.route("/", methods=["GET", "POST"])
def index():
    chart_data = None
    error_message = None

    if request.method == 'POST':
        if 'file' not in request.files:
            error_message = "No file part"
        else:
            file = request.files['file']
            if file.filename == '':
                error_message = "No selected file"
            elif not allowed_file(file.filename):
                error_message = "File type not allowed. Please upload an Excel file (.xls or .xlsx)."
            else:
                try:
                    filename = werkzeug.utils.secure_filename(file.filename) # Sanitize filename!
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    df = pd.read_excel(filepath)
                    chart_data = create_chart_data(df)
                except Exception as e:
                    app.logger.error(f"Error processing file: {e}")  # Log the error
                    error_message = "An error occurred while processing the file." # generic error for users

    # Get column names for dropdown selection from sample dataframe of user upload (if available)
    column_names = []

    if chart_data and 'labels' in chart_data.json:
         # get column names from dataframe on first upload to show in x/y axis selectors
        first_row = df.iloc[0].to_dict() # get column names from data
        column_names = list(first_row.keys())

    return render_template("index.html", chart_data=chart_data, error_message=error_message, column_names=column_names)



if __name__ == "__main__":
    app.run(debug=True) # NEVER set debug=True in production