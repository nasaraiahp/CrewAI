from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import os
import werkzeug

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file")

        if file and allowed_file(file.filename):
            try:
                filename = werkzeug.utils.secure_filename(file.filename) # Sanitize filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                df = pd.read_excel(filepath)
                location_counts = df.groupby('Location Name')['Employee ID'].count().reset_index()
                location_counts.columns = ['Location Name', 'Employee Count']

                fig = px.bar(location_counts, x='Location Name', y='Employee Count',
                             title='Employee Count by Location',
                             labels={'Employee Count': 'Number of Employees'})
                graph_html = fig.to_html(full_html=False)
                return render_template('index.html', graph=graph_html)

            except (pd.errors.ParserError, ValueError) as e:  # Catch specific Excel read errors
                return render_template('index.html', error=f"Invalid Excel file: {e}")
            except Exception as e:
                return render_template('index.html', error=f"Error processing file: {e}")  # Handle other potential errors


        else:
             return render_template('index.html', error="File type not allowed. Please upload .xls or .xlsx")


    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)