# app.py
import os
from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import pandas as pd
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

# Initialize database if it doesn't exist
os.makedirs(app.instance_path, exist_ok=True)
if not os.path.exists(DATABASE):
    init_db()


# Populate database with dummy data (run once initially)
@app.route('/init_data')
def init_data():
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        try:
            sales_data = [
                ('Product A', 100, 5000),
                ('Product B', 150, 7500),
                ('Product C', 80, 4000),
                ('Product D', 120, 6000),
                ('Product E', 200, 10000)
            ]
            cur.executemany("INSERT INTO sales (product, sales_quantity, sales_amount) VALUES (?, ?, ?)", sales_data)
            db.commit()
            return "Data initialized!"
        except Exception as e:  # Handle exceptions properly
            db.rollback() # Rollback on error to avoid partial updates
            return f"Error: {e}"


@app.route('/')
def index():
    with app.app_context():
        db = get_db()
        df = pd.read_sql_query("SELECT * FROM sales", db)


    # Bar chart
    bar_chart = go.Figure(data=[go.Bar(x=df['product'], y=df['sales_amount'])])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Pie chart
    pie_chart = go.Figure(data=[go.Pie(labels=df['product'], values=df['sales_quantity'])])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    app.run(debug=True)