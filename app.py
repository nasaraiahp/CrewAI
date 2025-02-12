from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas as pd
import plotly.express as px
import os
import werkzeug  # For secure filenames

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

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

        if file and allowed_file(file.filename):
            filename = werkzeug.utils.secure_filename(file.filename) # Secure filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                df = pd.read_excel(filepath)
                # ... (Chart creation code - same as before) ...
                return render_template('dashboard.html', chart1=chart1_json, chart2=chart2_json, chart3=chart3_json)
            except Exception as e:
                return render_template('error.html', error_message=str(e)) # Dedicated error page
        else:
            return render_template('error.html', error_message="Invalid file type. Please upload an Excel file.")

    return render_template('upload.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production!