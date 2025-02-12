from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import os
import werkzeug

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}  # Allowed file extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)  # Redirect if no file part

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)   # Redirect if no selected file

        if file and allowed_file(file.filename):
            try:
                filename = werkzeug.utils.secure_filename(file.filename) # Sanitize filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                df = pd.read_excel(filepath)
                charts = []
                for col in df.columns:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        fig = px.histogram(df, x=col, title=f"Distribution of {col}")
                        charts.append(fig.to_html(full_html=False))
                return render_template('dashboard.html', charts=charts)
            except Exception as e:
                return render_template('error.html', error_message=str(e)) # Dedicated error page

        else: return render_template('error.html', error_message="File type not allowed. Please upload xlsx or xls files.")
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)