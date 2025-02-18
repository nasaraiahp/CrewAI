from flask import Flask, render_template, request, jsonify
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Database configuration (better practice than global variable)
app.config['DATABASE'] = os.path.join(app.instance_path, 'sales_data.db')  # Store in instance folder
os.makedirs(app.instance_path, exist_ok=True)  # Ensure instance folder exists


def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    with get_db_connection() as conn:  # Use with statement for automatic closing
        sales_data = conn.execute('SELECT product, sales, region FROM sales').fetchall() # Only select needed columns

    bar_chart = create_bar_chart(sales_data)
    pie_chart = create_pie_chart(sales_data)

    return render_template('index.html', bar_graphJSON=bar_chart, pie_graphJSON=pie_chart)


def create_bar_chart(data):
    # Using list comprehensions is efficient
    products = [row['product'] for row in data]
    sales = [row['sales'] for row in data]

    fig = go.Figure(data=[go.Bar(x=products, y=sales)])
    fig.update_layout(title_text='Product Sales')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_pie_chart(data):
    regions = [row['region'] for row in data]
    sales = [row['sales'] for row in data]

    fig = go.Figure(data=[go.Pie(labels=regions, values=sales)])
    fig.update_layout(title_text='Sales by Region')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == '__main__':
    app.run(debug=False) # Disable debug mode in production