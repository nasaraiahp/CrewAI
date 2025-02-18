# app.py (Flask application)
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) # Add a secret key for session management

# Database configuration
DATABASE = 'sales_data.db'

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

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sales_dashboard')
def sales_dashboard():
    # Use parameterized queries to prevent SQL injection
    bar_chart_data = query_db("SELECT product_category, SUM(sales) AS total_sales FROM sales GROUP BY product_category")
    pie_chart_data = query_db("SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region")

    # Create charts
    bar_chart = go.Figure(data=[go.Bar(x=[row['product_category'] for row in bar_chart_data],
                                      y=[row['total_sales'] for row in bar_chart_data])])
    bar_chart.update_layout(title_text='Sales by Product Category')
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_chart = go.Figure(data=[go.Pie(labels=[row['region'] for row in pie_chart_data],
                                      values=[row['total_sales'] for row in pie_chart_data])])
    pie_chart.update_layout(title_text='Sales by Region')
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('sales_dashboard.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

if __name__ == '__main__':
    app.run(debug=True) # Never enable debug mode in production