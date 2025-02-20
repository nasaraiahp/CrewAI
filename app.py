# app.py
import os
from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Database setup and connection management
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access data by column name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def insert_dummy_data():  # Separate function for data insertion
    with app.app_context():
        db = get_db()
        dummy_data = [
            ('Product A', 'Electronics', 120),
            ('Product B', 'Clothing', 85),
            ('Product C', 'Electronics', 200),
            ('Product D', 'Books', 50),
            ('Product E', 'Clothing', 150),
            ('Product F', 'Books', 70),
            ('Product G', 'Electronics', 250),
            ('Product H', 'Clothing', 100)
        ]
        db.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
        db.commit()


# Ensure instance folder exists and create/populate the database on first run
os.makedirs(app.instance_path, exist_ok=True)
if not os.path.exists(DATABASE):  # Check if the database file exists
    init_db()
    insert_dummy_data()




@app.route('/')
def index():
    db = get_db()
    df = pd.read_sql_query("SELECT * FROM sales", db)  # Use db from get_db()

    # ... (chart creation code remains the same)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    app.run(debug=True)  # Consider setting debug=False in production