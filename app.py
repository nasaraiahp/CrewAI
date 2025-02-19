# app.py
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Database setup
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

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

# Initialize the database if it doesn't exist
if not os.path.exists(DATABASE):
    os.makedirs(app.instance_path, exist_ok=True) # Ensure instance path exists
    init_db()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def populate_db(): # Adds some dummy data ONLY if table is empty
    if not query_db('SELECT * FROM sales LIMIT 1'):
        sales_data = [
            ('Product A', 120, 'North'),
            ('Product B', 80, 'East'),
            ('Product C', 150, 'West'),
            ('Product A', 50, 'South'),
            ('Product B', 100, 'North'),
            ('Product C', 75, 'East'),
            ('Product D', 200, 'West'),
            ('Product E', 90, 'South'),
        ]
        db = get_db()
        db.executemany('INSERT INTO sales (product, sales_quantity, sales_region) VALUES (?, ?, ?)', sales_data)
        db.commit()



@app.route('/')
def index():
    populate_db()  # Populate only if the table is empty

    # Bar chart data
    bar_data = query_db('SELECT product, SUM(sales_quantity) FROM sales GROUP BY product')
    bar_labels = [row[0] for row in bar_data]
    bar_values = [row[1] for row in bar_data]

    bar_chart = go.Figure(data=[go.Bar(x=bar_labels, y=bar_values)])
    bar_chart_JSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Pie chart data
    pie_data = query_db('SELECT sales_region, SUM(sales_quantity) FROM sales GROUP BY sales_region')
    pie_labels = [row[0] for row in pie_data]
    pie_values = [row[1] for row in pie_data]

    pie_chart = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values)])
    pie_chart_JSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_JSON, pie_chart=pie_chart_JSON)


if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True) #Corrected instance path creation
    app.run(debug=True)