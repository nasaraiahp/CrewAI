# app.py (Flask application)
from flask import Flask, render_template
import sqlite3
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Database setup (best practice: store sensitive data like database paths securely)
DATABASE = os.environ.get("DATABASE_URL") or "sales_data.db"  # Use environment variable or default

# Function to get a database connection (with better error handling and context management)
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database error: {e}") # Log the error for debugging
        return None # Return None to handle the error gracefully in the calling function



@app.route('/')
def index():
    conn = get_db_connection()
    if conn is None:
        return "Database connection error", 500 # Return an error response to the user

    try:
        sales_data = conn.execute('SELECT product, sales FROM sales_data').fetchall()
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return "Error retrieving data", 500  # Return an error response
    finally:
        conn.close() # Ensure connection is always closed, even if error occurs


    # Prepare data for Plotly charts
    products = [row['product'] for row in sales_data]
    sales = [row['sales'] for row in sales_data]

    # Create charts (no changes needed here)
    bar_chart = go.Figure(data=[go.Bar(x=products, y=sales)])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_chart = go.Figure(data=[go.Pie(labels=products, values=sales)])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

if __name__ == '__main__':
    app.run(debug=False) # Disable debug mode in production