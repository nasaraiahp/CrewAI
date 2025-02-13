import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly.io as pio
import secrets
import werkzeug

app = Flask(__name__)

# Securely generate a secret key (important for production)
app.secret_key = secrets.token_hex(16)


# Set upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Secure file naming
def secure_filename(filename):
    return werkzeug.utils.secure_filename(filename)


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles the main route for file upload and graph display."""
    graph_html = None
    error = None  # Store error messages

    if request.method == 'POST':
        if 'file' not in request.files:
            error = "No file part"
        else:
            file = request.files['file']
            if file.filename == '':
                error = "No selected file"
            elif not allowed_file(file.filename):
                error = "File type not allowed. Please upload an Excel file (.xlsx or .xls)."
            else:
                try:
                    filename = secure_filename(file.filename) # Secure the filename
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    df = pd.read_excel(filepath)

                    # Example graph: Employee Count vs. Location Name (adapt as needed)
                    if 'Location Name' in df.columns and 'Employee ID' in df.columns:
                        location_counts = df.groupby('Location Name')['Employee ID'].count().reset_index()
                        fig = px.bar(location_counts, x='Location Name', y='Employee ID',
                                     title='Employee Count per Location')
                        graph_html = pio.to_html(fig, full_html=False)
                    else:
                       error = "The Excel file must contain 'Location Name' and 'Employee ID' columns." 

                except Exception as e:
                    error = f"Error processing file: {e}"


    # Pass the error or graph to the template outside the if block
    return render_template('index.html', graph=graph_html, error=error)




if __name__ == '__main__':
    app.run(debug=True)