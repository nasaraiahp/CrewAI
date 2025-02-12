# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import plotly.express as px
import secrets  # For generating secure filenames

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secure secret key for flash messages

UPLOAD_FOLDER = 'uploads'  # Dedicated uploads folder
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the uploads folder if it doesn't exist


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    charts = []
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            secure_filename = secrets.token_urlsafe(16) + '.' + file.filename.rsplit('.', 1)[1].lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename)
            file.save(filepath)  # Save the file securely

            try:
                df = pd.read_excel(filepath)

                # Chart creation (adapt columns as needed):
                fig1 = px.bar(df, x='Column1', y='Column2', title='Chart 1 Title')  # Bar chart
                charts.append(fig1.to_html(full_html=False, div_id='chart1'))

                fig2 = px.scatter(df, x='Column3', y='Column4', color='Column5', title='Chart 2 Title')  # Scatter plot
                charts.append(fig2.to_html(full_html=False, div_id='chart2'))


            except Exception as e:
                flash(f"Error processing file: {e}") # Provide informative error message
                return redirect(request.url)
            finally:
                os.remove(filepath) # Remove temporary file after processing

        else:
            flash("Invalid file type. Allowed types are .xlsx and .xls") # Inform user of invalid file type


    return render_template("index.html", charts=charts)




if __name__ == "__main__":
    app.run(debug=False)  # Disable debug mode in production