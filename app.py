# app.py
from flask import Flask, render_template
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Database setup
DATABASE = 'sales_data.db'  # Store database name as a constant

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access data by column name
    return conn

def create_tables():
    """Creates the necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT PRIMARY KEY,  -- Add primary key for efficiency
            sales INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_dummy_data():
    """Inserts dummy data if the table is empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:  # Check if table is empty
        dummy_data = [
            ('Product A', 1200),
            ('Product B', 850),
            ('Product C', 1550),
            ('Product D', 900),
            ('Product E', 1100),
        ]
        cursor.executemany("INSERT INTO sales VALUES (?, ?)", dummy_data)
        conn.commit()
    conn.close()


@app.route('/')
def index():
    create_tables()
    insert_dummy_data()

    conn = get_db_connection()
    sales_data = conn.execute("SELECT * FROM sales").fetchall()
    conn.close()

    bar_chart = go.Figure(data=[go.Bar(x=[row['product'] for row in sales_data],
                                       y=[row['sales'] for row in sales_data])])  # Use column names
    bar_chart_JSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)


    pie_chart = go.Figure(data=[go.Pie(labels=[row['product'] for row in sales_data],
                                       values=[row['sales'] for row in sales_data])])   # Use column names
    pie_chart_JSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_graphJSON=bar_chart_JSON, pie_graphJSON=pie_chart_JSON)


if __name__ == '__main__':
    app.run(debug=True)