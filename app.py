# app.py (Flask application)
import os
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Database setup and connection management
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

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def populate_db():
    with app.app_context():
        db = get_db()
        dummy_data = [
            ('Product A', 120),
            ('Product B', 85),
            ('Product C', 150),
            ('Product D', 100),
            ('Product E', 70),
        ]
        db.executemany("INSERT OR IGNORE INTO sales (product, sales_quantity) VALUES (?, ?)", dummy_data)
        db.commit()


# Ensure the database exists and is initialized, then populate with data
os.makedirs(app.instance_path, exist_ok=True)  # Create instance folder if it doesn't exist
if not os.path.exists(DATABASE):
    init_db()
    populate_db()



@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT product, sales_quantity FROM sales")
    sales_data = cursor.fetchall()

    products = [row[0] for row in sales_data]
    quantities = [row[1] for row in sales_data]

    # Create bar chart
    bar_chart = go.Figure(data=[go.Bar(x=products, y=quantities)])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Create pie chart
    pie_chart = go.Figure(data=[go.Pie(labels=products, values=quantities)])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

if __name__ == '__main__':
    app.run(debug=True)