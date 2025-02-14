from flask import Flask, render_template, request
import sqlite3
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import os

app = Flask(__name__)
DATABASE = 'sales_data.db'  # Define database name globally

# Database setup (create and populate if it doesn't exist)
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
                product TEXT,
                category TEXT,
                sales_quantity INTEGER,
                sales_amount REAL
            )
        ''')

def insert_dummy_data():
    """Inserts dummy data if the table is empty."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales")
        if cursor.fetchone()[0] == 0:
            dummy_data = [
                ('Product A', 'Electronics', 100, 5000),
                ('Product B', 'Clothing', 50, 2500),
                ('Product C', 'Electronics', 75, 3750),
                ('Product D', 'Clothing', 120, 6000),
                ('Product E', 'Books', 200, 4000),
                ('Product F', 'Books', 80, 1600),
                ('Product G', 'Electronics', 60, 3000)
            ]
            cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", dummy_data)


# Initialize database on app startup
@app.before_first_request
def init_db():
    """Initializes the database on the first request."""
    create_table()
    insert_dummy_data()

# ... (rest of the code remains largely the same, but uses get_db_connection())
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bar_chart")
def bar_chart():
    with get_db_connection() as conn:
        df = pd.read_sql_query("SELECT product, sales_quantity FROM sales", conn)

    # ... (plotting code remains the same)

@app.route("/pie_chart")
def pie_chart():
    with get_db_connection() as conn:
        df = pd.read_sql_query("SELECT category, SUM(sales_amount) AS total_sales FROM sales GROUP BY category", conn)
    # ... (plotting code remains the same)



if __name__ == "__main__":
    app.run(debug=True)