from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = 'sales_data.db'  # Define database path

# Database setup (run only once)
def initialize_database():
    with app.app_context():  # Use app context for database operations
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                product TEXT,
                category TEXT,
                sales_quantity INTEGER
            )
        ''')
        dummy_data = [
            ('Product A', 'Electronics', 120),
            ('Product B', 'Clothing', 85),
            ('Product C', 'Electronics', 200),
            ('Product D', 'Books', 150),
            ('Product E', 'Clothing', 50),
            ('Product F', 'Books', 250),
            ('Product G', 'Electronics', 100)
        ]
        cursor.executemany("INSERT OR IGNORE INTO sales VALUES (?, ?, ?)", dummy_data)
        conn.commit()


# Database connection management using `g` object
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


initialize_database()  # Initialize the database

@app.route('/')
def dashboard():
    conn = get_db() # Use get_db to manage database connections
    cursor = conn.cursor()
    cursor.execute("SELECT product, sales_quantity FROM sales")
    bar_data = cursor.fetchall()
    cursor.execute("SELECT category, SUM(sales_quantity) FROM sales GROUP BY category")
    pie_data = cursor.fetchall()

    # ... (rest of the code remains the same as before)
    # ...

if __name__ == '__main__':
    app.run(debug=False) # Disable debug mode in production