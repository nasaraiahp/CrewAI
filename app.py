from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__, template_folder='templates')  # Explicit template folder
DATABASE = os.path.join(app.instance_path, 'sales.db') # Define database path relative to the app's instance folder

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # Access data by name instead of index
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
        # Query data for bar chart
        sales_by_product = query_db('SELECT product, SUM(sales) AS total_sales FROM sales_data GROUP BY product')
        product_names = [row['product'] for row in sales_by_product]
        sales_figures = [row['total_sales'] for row in sales_by_product]

        bar_chart = go.Figure(data=[go.Bar(x=product_names, y=sales_figures)])
        bar_chart.update_layout(title='Sales by Product')
        bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

        # Query data for pie chart
        sales_by_region = query_db('SELECT region, SUM(sales) AS total_sales FROM sales_data GROUP BY region')
        region_names = [row['region'] for row in sales_by_region]
        region_sales = [row['total_sales'] for row in sales_by_region]

        pie_chart = go.Figure(data=[go.Pie(labels=region_names, values=region_sales)])
        pie_chart.update_layout(title='Sales by Region')
        pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Log the error for debugging
        return "A database error occurred.", 500 # Return a generic error message to the user
    except Exception as e:
        print(f"An unexpected error occurred: {e}") # Log the error for debugging
        return "An unexpected error occurred.", 500  # Return a generic error message to the user


if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True) # Ensure the instance folder exists
    app.run(debug=False) # Disable debug mode in production