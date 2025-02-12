from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import os
import secrets
import werkzeug.utils

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}  # Allow only Excel files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = secrets.token_hex(16) # Generate a secret key for secure sessions

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)  # Redirect if no file part

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url) # Redirect if no selected file

        if file and allowed_file(file.filename):  # Check allowed file type
            filename = werkzeug.utils.secure_filename(file.filename) # Sanitize filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                df = pd.read_excel(filepath)
                # ... (chart creation code remains the same) ...

                chart1.write_html(os.path.join('templates', 'chart1.html')) # Save inside templates folder
                chart2.write_html(os.path.join('templates', 'chart2.html')) # Save inside templates folder

                return redirect(url_for('display_charts'))  # Use url_for for cleaner redirects
            except Exception as e:
                return f"Error processing file: {e}"  # Consider more user-friendly error messages
    return render_template('upload.html')


@app.route('/charts')
def display_charts():
    chart1_path = os.path.join('templates', 'chart1.html') # Define relative paths for HTML files.
    chart2_path = os.path.join('templates', 'chart2.html')

    if not (os.path.exists(chart1_path) and os.path.exists(chart2_path)):
        return "Charts not available. Please upload a file first." # Handle missing charts

    return render_template('charts.html', chart1=chart1_path, chart2=chart2_path)


if __name__ == '__main__':
    app.run(debug=False) # Disable debug mode in production