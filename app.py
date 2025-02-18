# app.py (Flask application)
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = 'sales_data.db'  # Define database name globally

# Database connection and data retrieval using application context
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


# Insert sample data if table is empty
def insert_sample_data():
    with app.app_context():
        if not query_db('SELECT * FROM sales LIMIT 1'): # more efficient check if table is empty
            sample_data = [
                ('Product A', 1500), ('Product B', 1200), ('Product C', 900),
                ('Product D', 2100), ('Product E', 1800)
            ]
            get_db().executemany('INSERT INTO sales (product, sales) VALUES (?, ?)', sample_data)
            get_db().commit()


# Routes
@app.route('/')
def index():
    insert_sample_data()  # Ensure sample data exists
    sales_data = query_db('SELECT * FROM sales')

    # Create charts using list comprehensions for efficiency
    bar_chart = go.Figure(data=[go.Bar(x=[row['product'] for row in sales_data],
                                       y=[row['sales'] for row in sales_data])])
    pie_chart = go.Figure(data=[go.Pie(labels=[row['product'] for row in sales_data],
                                       values=[row['sales'] for row in sales_data])])

    # Use dumps once for each chart
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    app.run(debug=True)