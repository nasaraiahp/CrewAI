from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import io
import matplotlib.pyplot as plt
import base64
import werkzeug
from werkzeug.utils import secure_filename
import secrets

app = Flask(__name__)

# Securely generate a secret key for session management
app.secret_key = secrets.token_hex(16) #  Use secrets module for strong random key

# File upload settings - using a more secure approach
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit
ALLOWED_EXTENSIONS = {'xlsx', 'xls'} # Allow only Excel files

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if not allowed_file(file.filename): # Check for allowed file types
           return jsonify({'error': 'File type not allowed. Please upload an Excel file.'})


        try:
            # Securely handle filename and save uploaded file
            filename = secure_filename(file.filename) # Use secure_filename 
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)


            file.save(file_path)



            # Read Excel data using pandas
            df = pd.read_excel(file_path)

            # Generate charts (example using matplotlib)
            charts = []
            for column in df.columns:
                if pd.api.types.is_numeric_dtype(df[column]):  # Only create charts for numeric columns
                    plt.figure()  # Create a new figure for each chart
                    plt.plot(df[column])
                    plt.title(column)
                    plt.xlabel('Index')
                    plt.ylabel('Value')

                    # Save the plot to a BytesIO object
                    img = io.BytesIO()
                    plt.savefig(img, format='png')
                    img.seek(0)

                    # Encode the image as base64
                    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

                    charts.append({'title': column, 'url': plot_url})
                    plt.close() # Close plot to free resources

            return render_template('dashboard.html', charts=charts)


        except Exception as e:
            return jsonify({'error': str(e)})

    return render_template('upload.html')



if __name__ == '__main__':
    app.run(debug=True) # Never run with debug=True in production!