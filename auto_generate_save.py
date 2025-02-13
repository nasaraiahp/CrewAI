from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import plotly
import plotly.express as px
import json
import werkzeug

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Secure file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file")

        if file and allowed_file(file.filename):
            try:
                filename = werkzeug.utils.secure_filename(file.filename) # Secure filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                df = pd.read_excel(filepath)

                # Graph 1: Employee Count vs. Location Name
                loc_emp_count = df.groupby('Location Name')['Employee ID'].count().reset_index()
                fig1 = px.bar(loc_emp_count, x='Location Name', y='Employee ID', title='Employee Count per Location')
                graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

                # Graph 2: Sum of Hours vs. Department
                dept_hours = df.groupby('Department')['Hours'].sum().reset_index()
                fig2 = px.bar(dept_hours, x='Department', y='Hours', title='Total Hours per Department')
                graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

                return render_template('index.html', graph1JSON=graph1JSON, graph2JSON=graph2JSON)

            except Exception as e:
                return render_template('index.html', error=f"An error occurred during processing: {e}")  # More specific error message

        else:
            return render_template('index.html', error="Invalid file type. Please upload an Excel file.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)