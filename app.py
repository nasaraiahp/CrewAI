# app.py (Flask application)
from flask import Flask, render_template
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Database configuration
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

def get_db():
    """Returns a database connection."""
    db = getattr(g, '_database', None)  # Use g to avoid global variables
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access data by column name
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection after each request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def init_app(app):
    """Initializes the application."""
    app.teardown_appcontext(close_connection) # Register close_connection
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Initialize the database if it doesn't exist
    if not os.path.exists(DATABASE):
        init_db()

def populate_sales_table(db):  # Inject db connection
    """Populates the sales table with initial data if empty."""
    cursor = db.execute("SELECT COUNT(*) FROM sales").fetchone()
    if cursor[0] == 0: # Check if table is empty
        data = [
            ('Product A', 100, 1500.00),
            ('Product B', 150, 2250.00),
            ('Product C', 80, 1200.00),
            ('Product D', 120, 1800.00),
            ('Product E', 90, 1350.00),
        ]
        db.executemany("INSERT INTO sales (product, sales_quantity, sales_revenue) VALUES (?, ?, ?)", data)
        db.commit()



@app.route('/')
def index():
    db = get_db()  # Get the database connection
    populate_sales_table(db)  # Populate data if necessary

    sales_data = db.execute("SELECT product, sales_quantity, sales_revenue FROM sales").fetchall()

    # ... (chart creation code remains the same)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

# Call the init_app function to initialize the app
init_app(app)

if __name__ == '__main__':
    app.run(debug=True)