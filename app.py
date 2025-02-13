from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import sqlite3
import os

app = Flask(__name__)

# Database configuration (better practice to store outside the main code)
DATABASE = os.path.join(app.instance_path, 'sales.db')  # Store DB in instance folder

# Create the instance folder if it doesn't exist
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    sales_data = pd.DataFrame() # Initialize as empty DataFrame
    graphJSON = None
    try:
        if request.method == 'POST': # Handle data upload
            file = request.files['file']
            if file:
                sales_data = pd.read_csv(file)  # Read from CSV

                # Sanitize/validate the data before inserting into the database
                # ... (Add data validation logic here based on your specific requirements,
                # e.g., check data types, remove illegal characters, etc.)

                sales_data.to_sql('sales', conn, if_exists='replace', index=False) # Replace table data


        # Query the database (only after potential upload)
        sales_data = pd.read_sql_query("SELECT Price, `Location Name`, `Product Name`, `Product ID` FROM sales", conn)


        if not sales_data.empty:
             fig = px.histogram(sales_data, x="Location Name", y="Price", title="Price Distribution by Location")
             graphJSON = fig.to_json()


    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return render_template('error.html', error_message=str(e))

    finally:
        conn.close()

    return render_template('index.html', graphJSON=graphJSON)



if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production!