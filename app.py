# app.py
from flask import Flask, render_template
import sqlite3
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Database setup
DATABASE = 'sales_data.db'  # Define database name as a constant

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access data by column name
    return conn

def create_table():
    """Creates the sales table if it doesn't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                product TEXT UNIQUE,  -- Ensure product names are unique
                sales_quantity INTEGER
            )
        ''')

def insert_dummy_data():
    """Inserts dummy data into the sales table."""
    dummy_data = [
        ('Product A', 120),
        ('Product B', 80),
        ('Product C', 150),
        ('Product D', 50),
        ('Product E', 100)
    ]
    try: # Handle potential IntegrityError if unique constraint is violated.
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany("INSERT INTO sales VALUES (?,?)", dummy_data)
    except sqlite3.IntegrityError:
        pass # Ignore error if data already exists.  This is cleaner than INSERT OR IGNORE


@app.route('/')
def index():
    if not os.path.exists(DATABASE): # Check if the database exists
        create_table()
        insert_dummy_data()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        sales_data = cursor.execute("SELECT * FROM sales").fetchall()

    products = [row['product'] for row in sales_data] # Use column names
    sales_quantities = [row['sales_quantity'] for row in sales_data]

    # Create charts
    bar_chart = go.Figure(data=[go.Bar(x=products, y=sales_quantities)])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_chart = go.Figure(data=[go.Pie(labels=products, values=sales_quantities)])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    app.run(debug=True) # ONLY set debug to true for development