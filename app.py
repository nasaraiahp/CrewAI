# app.py (Flask backend)
from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access data by column name
    return conn

def init_db():
    """Initializes the database and creates the sales table."""
    with app.app_context():  # Access app context for instance path
        conn = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()
        conn.close()

# Check if the instance folder exists and create if not.
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Initialize database if it doesn't exist.
if not os.path.exists(DATABASE):
    init_db()

def insert_dummy_data():
    """Inserts dummy data into the sales table if it's empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:
        dummy_data = [
            ('Product A', 'Electronics', 100, 5000.00),
            ('Product B', 'Clothing', 50, 2500.00),
            ('Product C', 'Electronics', 75, 3750.00),
            ('Product D', 'Books', 120, 2400.00),
            ('Product E', 'Clothing', 90, 4500.00),
        ]
        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", dummy_data)
        conn.commit()
    conn.close()


@app.route('/')
def index():
    insert_dummy_data() # Ensure dummy data exists before rendering the template
    return render_template('index.html')

@app.route('/data')
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product, sales_quantity, category, sales_revenue FROM sales")
    rows = cursor.fetchall()
    conn.close()

    # Improved data handling using dictionary comprehension and list comprehension
    data = {
        'products': [row['product'] for row in rows],
        'sales_quantities': [row['sales_quantity'] for row in rows],
        'categories': list({row['category'] for row in rows}),  # Efficiently get unique categories
        'sales_revenues_by_category': {}  # Aggregate revenue by category
    }

    # Aggregate revenue by category efficiently using a loop
    for row in rows:
        category = row['category']
        revenue = row['sales_revenue']
        data['sales_revenues_by_category'][category] = data['sales_revenues_by_category'].get(category, 0) + revenue

    return jsonify(data)  # Return JSON data


if __name__ == '__main__':
    app.run(debug=True)