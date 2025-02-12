from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import json
import werkzeug
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}  # Allowed file extensions
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
            return redirect(request.url)  # Redirect on missing file

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url) # Redirect on no selected file

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # Secure filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                df = pd.read_excel(filepath)
                chart_data = generate_charts(df)
                return render_template('dashboard.html', chart_data=chart_data)
            except Exception as e:
                 # Log the error for debugging
                print(f"Error processing file: {e}") 
                return render_template('error.html', error_message=str(e)) # Show generic error

    return render_template('upload.html')

def generate_charts(df):
    # ... (same as before)

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production