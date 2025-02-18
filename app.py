# app.py
import os
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Database setup
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
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

# Check if the instance folder exists and create if it doesn't
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

# Initialize the database if it doesn't exist
if not os.path.exists(DATABASE):
    init_db()

# Populate database with dummy data (run only once after init_db) - commented out after initial run
# def populate_database():
#     with app.app_context():
#         db = get_db()
#         sample_data = [
#             ('Product A', 150),
#             ('Product B', 200),
#             ('Product C', 100),
#             ('Product D', 250),
#             ('Product E', 180),
#         ]
#         db.executemany('INSERT INTO sales (product, sales_quantity) VALUES (?, ?)', sample_data)
#         db.commit()


# populate_database() # Uncomment to populate, then comment out again


@app.route('/')
def index():
    db = get_db()
    sales_data = db.execute('SELECT * FROM sales').fetchall()
    # ... (rest of the chart creation code remains the same)


if __name__ == '__main__':
    app.run(debug=True)