# app.py (Flask application)
import os
from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import plotly
import json

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Database connection (using application context)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access data by column names
    return db

# Close database connection at the end of the request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Execute database queries
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    sales_data = query_db('SELECT * FROM sales')

    # Data for bar chart
    products = [row['product'] for row in sales_data]
    sales = [row['sales'] for row in sales_data]

    bar_chart = go.Figure(data=[go.Bar(x=products, y=sales)])
    bar_chart.update_layout(title="Sales by Product")
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Data for pie chart (now dynamically retrieved – example data removed)
    region_sales = query_db("SELECT region, SUM(sales) AS total_sales FROM regional_sales GROUP BY region") # Query example, adjust as needed.
    regions = [row['region'] for row in region_sales]
    sales_distribution = [row['total_sales'] for row in region_sales]

    pie_chart = go.Figure(data=[go.Pie(labels=regions, values=sales_distribution)])
    pie_chart.update_layout(title="Sales Distribution by Region")
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

# Create the instance folder if it doesn't exist
os.makedirs(app.instance_path, exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)  # Consider setting debug=False for production