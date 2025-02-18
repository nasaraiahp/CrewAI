# app.py (Flask application)
from flask import Flask, render_template, request, jsonify
import sqlite3
import plotly.graph_objs as go
import json
import pandas as pd
import os

app = Flask(__name__)

# Database setup
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access data by column name
    return conn

# Create the database if it doesn't exist
def create_database():
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    conn = get_db_connection()
    with app.open_resource('sales_data.sql', mode='r') as f:
        conn.executescript(f.read())  # Execute SQL schema
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM sales", conn)
    except Exception as e:  # Handle potential database errors
        print(f"Database error: {e}")  # Log error for debugging
        return jsonify({"error": "Database error"}), 500  # Return error to client
    finally:
        conn.close()  # Ensure connection is closed even if error


    return df.to_json(orient='records')


@app.route('/bar_chart_data')
def bar_chart_data():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT product_category, SUM(sales_amount) AS total_sales FROM sales GROUP BY product_category", conn)
        fig = go.Figure(data=[go.Bar(x=df['product_category'], y=df['total_sales'])])
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    except Exception as e:  # Handle potential database errors
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()



@app.route('/pie_chart_data')
def pie_chart_data():
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT sales_region, SUM(sales_amount) AS total_sales FROM sales GROUP BY sales_region", conn)
        fig = go.Figure(data=[go.Pie(labels=df['sales_region'], values=df['total_sales'], hole=.3)])
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    except Exception as e:  # Handle potential database errors
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    create_database()  # Create database on startup if it doesn't exist.
    app.run(debug=True) # Set debug=False for Production