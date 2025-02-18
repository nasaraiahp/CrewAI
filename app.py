from flask import Flask, render_template
import sqlite3
import plotly.graph_objs as go
import pandas as pd
import os

app = Flask(__name__)

DATABASE = 'sales_data.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access data by column name
    return conn

def create_database():
    """Creates the database table if it doesn't exist and populates with initial data."""
    if not os.path.exists(DATABASE):  # Check if database file exists. Create if not.
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE sales (
                region TEXT,
                product TEXT,
                sales_amount REAL
            )
        ''')

        sample_data = [
            ('North', 'Product A', 1200),
            ('North', 'Product B', 850),
            ('East', 'Product A', 1500),
            ('East', 'Product C', 1000),
            ('South', 'Product B', 1100),
            ('South', 'Product C', 900),
            ('West', 'Product A', 1800),
            ('West', 'Product B', 700),
            ('West', 'Product D', 1300),
        ]

        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", sample_data)
        conn.commit()
        conn.close()

@app.route('/')
def index():
    create_database()
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()

    bar_chart = go.Figure(data=[go.Bar(x=df['region'], y=df['sales_amount'])])
    bar_chart.update_layout(title='Sales by Region')
    bar_chart_json = bar_chart.to_json()

    pie_chart = go.Figure(data=[go.Pie(labels=df['product'], values=df['sales_amount'])])
    pie_chart.update_layout(title='Sales by Product')
    pie_chart_json = pie_chart.to_json()

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    app.run(debug=True)