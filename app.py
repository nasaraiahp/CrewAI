# app.py
from flask import Flask, render_template
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Configuration (Best practice to separate configuration)
app.config['DATABASE'] = os.path.join(app.root_path, 'sales_data.db')  # Store DB within app directory

# Database connection (using app context for better resource management)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row  # For dictionary-like access
    return db

# Initialize database (using a dedicated function and try-except block)
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Check if database exists and initialize if not
def check_and_init_db():
    if not os.path.exists(app.config['DATABASE']):
        init_db()
        populate_db()  # Populate after initializing


# Populate database with dummy data
def populate_db():
    with app.app_context():
        db = get_db()
        dummy_data = [
            ('Product A', 'Electronics', 100, 5000),
            ('Product B', 'Clothing', 150, 3000),
            ('Product C', 'Books', 200, 4000),
            ('Product D', 'Electronics', 120, 6000),
            ('Product E', 'Clothing', 80, 2000),
            ('Product F', 'Books', 180, 3600),
        ]
        db.executemany('INSERT INTO sales VALUES (?, ?, ?, ?)', dummy_data)
        db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    check_and_init_db() # Initialize DB if it doesn't exist. Run only once
    db = get_db()
    
    bar_data = db.execute("SELECT product, sales_quantity FROM sales").fetchall()
    pie_data = db.execute("SELECT category, SUM(sales_amount) as total_sales FROM sales GROUP BY category").fetchall()

    bar_chart = create_bar_chart(bar_data)
    pie_chart = create_pie_chart(pie_data)
    return render_template('index.html', bar_chart=bar_chart, pie_chart=pie_chart)


# ... (chart creation functions remain the same)

if __name__ == '__main__':
    app.run(debug=True)