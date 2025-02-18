from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import pandas as pd
import os

app = Flask(__name__)

# Database configuration
DATABASE = os.path.join(app.root_path, 'sales_data.db')  # Store DB in app's directory

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


@app.route('/')
def index():
    try:
        # Query data for bar chart using parameterized query
        bar_data = pd.read_sql_query("SELECT product, SUM(sales) AS total_sales FROM sales GROUP BY product", get_db())
        bar_fig = go.Figure(data=[go.Bar(x=bar_data['product'], y=bar_data['total_sales'])])
        bar_fig.update_layout(title='Total Sales by Product')
        bar_graphJSON = bar_fig.to_json()

        # Query data for pie chart using parameterized query
        pie_data = pd.read_sql_query("SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region", get_db())
        pie_fig = go.Figure(data=[go.Pie(labels=pie_data['region'], values=pie_data['total_sales'])])
        pie_fig.update_layout(title='Sales Distribution by Region')
        pie_graphJSON = pie_fig.to_json()

        return render_template('index.html', bar_graphJSON=bar_graphJSON, pie_graphJSON=pie_graphJSON)

    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return "An error occurred", 500  # Return 500 error code


if __name__ == '__main__':
    app.run(debug=False) # Disable debug mode in production