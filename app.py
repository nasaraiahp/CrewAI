from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import plotly
import json
import pandas as pd
import os

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'sales_data.db')  # Store DB within app directory

# Database setup (using Flask's application context)
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

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Initialize the database if it doesn't exist
if not os.path.exists(DATABASE):
    init_db()

# Populate table (only if it's empty - prevents duplicate data on each run)
def populate_table():
    if not query_db('SELECT * FROM sales'): # Check if table is empty
        with app.app_context():
            data = [
                ('Product A', 15000),
                ('Product B', 22000),
                ('Product C', 18000),
                ('Product D', 25000),
                ('Product E', 12000),
            ]
            db = get_db()
            db.executemany("INSERT INTO sales VALUES (?,?)", data)
            db.commit()
populate_table()  # Call the function to populate if needed

# Routes
@app.route('/')
def index():
    with app.app_context(): #correct db handling in view
        df = pd.read_sql_query("SELECT * FROM sales", get_db())

        # ... (chart creation code - remains the same)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    app.run(debug=True)  # Keep debug mode for development