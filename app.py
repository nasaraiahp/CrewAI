import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for uploads (adjust as needed)
UPLOAD_FOLDER = 'uploads'  # Create this folder
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload directory exists


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Sanitize filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                df = pd.read_excel(filepath)

                # Chart creation (unchanged for brevity)
                chart1 = px.histogram(df, x="Location Name", title="Employee Count by Location")
                chart2 = px.bar(df.groupby("Month")["Employee ID"].count().reset_index(),
                               x="Month", y="Employee ID", title="Total Employees per Month")

                chart1_html = chart1.to_html(full_html=False, include_plotlyjs='cdn')
                chart2_html = chart2.to_html(full_html=False, include_plotlyjs='cdn')

                return render_template('charts.html', chart1=chart1_html, chart2=chart2_html)


            except Exception as e:
                return render_template('index.html', error=str(e))
        else:
            return render_template('index.html', error="Invalid file type")


    return render_template('index.html', error=None)


if __name__ == '__main__':
    app.run(debug=True) # Set debug=False in production