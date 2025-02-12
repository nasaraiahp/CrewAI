from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
from werkzeug.utils import secure_filename
import os
import secrets  # For generating secure random filenames

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """Generates a secure, random filename to prevent collisions and overwriting."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(filename)
    return random_hex + f_ext


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file")
        if not allowed_file(file.filename):
            return render_template('index.html', error="File type not allowed. Please upload an Excel file.")

        if file and allowed_file(file.filename):

            try:  # Limit file size
                file.read()  # Read the file into memory to check the size against config
                file.seek(0) # Reset after reading
            except Exception as e:
                 return render_template('index.html', error=f"File too large or other read error: {e}")




            filename = secure_filename(file.filename) 
            unique_filename = generate_unique_filename(filename) # Use the function
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)


            file.save(filepath)


            try:
                df = pd.read_excel(filepath, engine='openpyxl') # Explicitly use openpyxl

                # ... (Chart creation code remains the same)


                return render_template('index.html', chart1=chart1_html, chart2=chart2_html, chart3=chart3_html)
            except Exception as e:
                return render_template('index.html', error=f"Error processing file: {e}")

    return render_template('index.html')


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)  # Set debug=False for production