# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
from werkzeug.utils import secure_filename
import secrets  # Import secrets module

app = Flask(__name__)

# Generate a cryptographically secure secret key
SECRET_KEY = secrets.token_urlsafe(32)  # Improved security
app.secret_key = SECRET_KEY

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}  # Restrict file types
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)  # Handle missing file
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url) # Handle no selected file

        if file and allowed_file(file.filename):  # Check file extension
            filename = secure_filename(file.filename)  # Use secure filenames
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                df = pd.read_excel(filepath)
                charts = create_charts(df)
                return render_template('dashboard.html', charts=charts)
            except Exception as e:
                return render_template('error.html', error=str(e))
        else:
            return render_template('error.html', error="Invalid file type. Please upload an Excel file.")

    return render_template('upload.html')

def create_charts(df):
    charts = []  # Initialize charts list to handle potential missing columns
    try:
        chart1 = px.bar(df, x='column1', y='column2', title='Chart 1').to_html(full_html=False)
        charts.append(chart1)
        chart2 = px.scatter(df, x='column3', y='column4', title='Chart 2').to_html(full_html=False)
        charts.append(chart2)
        chart3 = px.pie(df, values='column5', names='column6', title='Chart 3').to_html(full_html=False)
        charts.append(chart3)

    except KeyError as e:  # Gracefully handle missing columns
         return render_template('error.html', error=f"Column missing in Excel: {e}") # More specific error

    return charts


if __name__ == '__main__':
    app.run(debug=False)  # Disable debug in production