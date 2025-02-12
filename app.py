from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import os
import werkzeug
from werkzeug.utils import secure_filename
import uuid

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
            return render_template('error.html', error="No file part")
        file = request.files['file']
        if file.filename == '':
            return render_template('error.html', error="No selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Sanitize filename
            # Add UUID to filename to prevent collisions and overwriting:
            filename = str(uuid.uuid4()) + "_" + filename

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                df = pd.read_excel(filepath)
                charts = create_charts(df)

                if isinstance(charts, list):  # Check if chart creation was successful
                     return render_template('dashboard.html', charts=charts)
                else: # create_charts may have returned a redirect to an error page due to issues
                     return charts

            except Exception as e:
                return render_template('error.html', error=f"Error processing file: {e}")

        else:
            return render_template('error.html', error="Invalid file type. Please upload an Excel file.")

    return render_template('upload.html')


def create_charts(df):
    try:
        # Explicitly specify column names – replace with your actual column names
        x_col = "col1"
        y_col = "col2"

        if x_col not in df.columns or y_col not in df.columns:
           raise KeyError(f"Column(s) missing from the sheet: {x_col if x_col not in df.columns else ''} {y_col if y_col not in df.columns else ''}")

        chart1 = px.bar(df, x=x_col, y=y_col, title='Chart 1').to_html(full_html=False)
        chart2 = px.scatter(df, x='col3', y='col4', title='Chart 2').to_html(full_html=False)
        chart3 = px.pie(df, values='col5', names='col6', title='Chart 3').to_html(full_html=False)  # Corrected

        return [chart1, chart2, chart3]
    except KeyError as e:

        return render_template("error.html", error=f"Column Missing from the sheet: {e}")
    except Exception as e:
        return render_template("error.html", error=f"Error creating charts: {e}")



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)