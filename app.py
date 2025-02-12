import os

import pandas as pd
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Configuration (Better to store sensitive information securely, e.g., environment variables)
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}  # Restrict allowed file types
UPLOAD_FOLDER = 'uploads'  # Dedicated folder for uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Create the uploads directory if it doesn't exist.


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_charts(df):
    # ... (chart creation logic remains the same)


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"  # Provide user feedback

        file = request.files['file']
        if file.filename == '':
            return "No selected file" # Provide better user feedback

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Sanitize filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                df = pd.read_excel(filepath)
                # ... (rest of the chart creation and rendering logic)
            except Exception as e: # Handle potential exceptions during file processing
                return f"Error processing file: {e}" # Provide specific error to the user
        else:
            return "File type not allowed. Please upload an Excel file." # Provide better user feedback


    # Handle GET request (initial display or when no file is uploaded yet)
    return render_template('dashboard.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production!