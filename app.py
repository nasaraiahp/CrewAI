# app.py (Flask application)
import sqlite3
import json

import plotly
import plotly.graph_objs as go
from flask import Flask, render_template, g

app = Flask(__name__)

# Database configuration
DATABASE = 'sales_data.db'

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


# Routes
@app.route('/')
def index():
    sales_by_product = query_db('SELECT product, SUM(sales) AS total_sales FROM sales GROUP BY product')
    sales_by_region = query_db('SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region')

    # Plotly charts
    bar_chart = create_bar_chart(sales_by_product, 'Sales by Product')
    pie_chart = create_pie_chart(sales_by_region, 'Sales by Region')

    return render_template('index.html', 
                           bar_chart=bar_chart,
                           pie_chart=pie_chart)

def create_bar_chart(data, title):
    fig = go.Figure(data=[go.Bar(
        x=[row['product'] for row in data],
        y=[row['total_sales'] for row in data]
    )], layout=go.Layout(title=title))
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_pie_chart(data, title):
     fig = go.Figure(data=[go.Pie(
        labels=[row['region'] for row in data],
        values=[row['total_sales'] for row in data]
    )], layout=go.Layout(title=title))
     return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)



if __name__ == '__main__':
    app.run(debug=True)