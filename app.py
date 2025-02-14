# app/app.py
import os
from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import json

app = Flask(__name__)

# Database setup
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Access data by name
    return conn

def init_db():
    with app.app_context():  # Ensures correct context for db access
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:  # Schema in separate file
            db.cursor().executescript(f.read())
        db.commit()

# Initialize the database if it doesn't exist
if not os.path.exists(DATABASE):
    os.makedirs(app.instance_path, exist_ok=True)  # Create instance folder if needed
    init_db()


def insert_dummy_data():  # Separate function for data insertion
    with app.app_context():
        db = get_db()
        dummy_data = [
            ('Product A', 'Electronics', 100, 5000),
            ('Product B', 'Clothing', 150, 3000),
            ('Product C', 'Electronics', 50, 2500),
            ('Product D', 'Clothing', 200, 4000),
            ('Product E', 'Books', 75, 1500)
        ]
        db.executemany("INSERT OR IGNORE INTO sales VALUES (?, ?, ?, ?)", dummy_data)
        db.commit()

# Call insert_dummy_data only if the table is empty
with app.app_context():
    db = get_db()
    if db.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == 0:
        insert_dummy_data()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    with app.app_context():
        db = get_db()
        df = pd.read_sql_query("SELECT * from sales", db)
        # No need to explicitly close db connection when using 'with'

        # Using list comprehensions for better efficiency
        sales_by_product = {row['product']: row['sales_amount'] for row in db.execute("SELECT product, SUM(sales_amount) as sales_amount FROM sales GROUP BY product").fetchall()}
        sales_by_category = {row['category']: row['sales_amount'] for row in db.execute("SELECT category, SUM(sales_amount) as sales_amount FROM sales GROUP BY category").fetchall()}

        return jsonify({
            'salesByProduct': sales_by_product,
            'salesByCategory': sales_by_category
        })


# app/schema.sql
DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    product TEXT,
    category TEXT,
    sales_quantity INTEGER,
    sales_amount REAL
);