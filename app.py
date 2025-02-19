from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Database configuration
DATABASE = os.path.join(app.instance_path, 'sales.db')  # Store DB in instance folder

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access data by column names
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


@app.route('/')
def index():
    sales_data = query_db('SELECT * FROM sales')

    # Create charts using list comprehensions for efficiency
    bar_chart = go.Figure(data=[go.Bar(x=[row['product'] for row in sales_data], y=[row['sales'] for row in sales_data])])
    pie_chart = go.Figure(data=[go.Pie(labels=[row['product'] for row in sales_data], values=[row['sales'] for row in sales_data])])

    # Convert chart data to JSON
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True)  # Ensure instance folder exists
    app.run(debug=False) # Disable debug mode in production