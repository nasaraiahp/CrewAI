# app.py
import sqlite3
import json
from flask import Flask, render_template, g
import plotly
import plotly.graph_objs as go

app = Flask(__name__)
DATABASE = 'sales_data.db'

# Database setup using a context manager for better resource management
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

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def create_tables():
    with app.app_context():  # Ensures the app context is available
        query_db('''
            CREATE TABLE IF NOT EXISTS sales (
                product TEXT,
                category TEXT,
                region TEXT,
                sales INTEGER
            )
        ''')
        get_db().commit()


def populate_dummy_data():
    with app.app_context():
        sample_data = [
            ('Product A', 'Electronics', 'North', 1500),
            ('Product B', 'Clothing', 'East', 1200),
            ('Product C', 'Electronics', 'West', 2000),
            # ... (rest of the data)
        ]
        query_db("INSERT INTO sales VALUES (?, ?, ?, ?)", sample_data, many=True)  # Use executemany equivalent
        get_db().commit()

# Create tables and populate data on startup (using app context)
create_tables()
populate_dummy_data()



@app.route('/')
def index():
    # Data for bar chart
    bar_data = query_db("SELECT product, SUM(sales) FROM sales GROUP BY product")
    bar_labels = [row[0] for row in bar_data]
    bar_values = [row[1] for row in bar_data]

    bar_chart = go.Figure(data=[go.Bar(x=bar_labels, y=bar_values)])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)


    # Data for pie chart
    pie_data = query_db("SELECT category, SUM(sales) FROM sales GROUP BY category")
    pie_labels = [row[0] for row in pie_data]
    pie_values = [row[1] for row in pie_data]

    pie_chart = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values)])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    app.run(debug=True)  # Consider removing debug=True in production