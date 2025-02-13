# app.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import sqlite3
import pandas as pd
from flask import Flask
import os

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Database Configuration (Best Practice: Use environment variables for sensitive data)
DATABASE_URL = os.environ.get("DATABASE_URL", "sales_data.db")  # Default to sales_data.db if no env variable

# SQL Query
query = "SELECT product_category, SUM(sales) AS total_sales FROM sales GROUP BY product_category"

# Function to read data from the database (better for managing connections)
def get_sales_data(db_url):
    conn = sqlite3.connect(db_url)
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:  # Ensures the connection is closed even if errors occur.
        conn.close()

df = get_sales_data(DATABASE_URL)  # Get data outside the callback for better performance.


app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),

    dcc.Graph(id='bar-chart'),

    dcc.Graph(id='pie-chart'),


])


@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('bar-chart', 'id') # dummy input to trigger initial drawing - we'll improve this later.
)
def update_charts(dummy_input):
    # The data is already loaded globally so this callback is efficient now.
    bar_fig = px.bar(df, x='product_category', y='total_sales', title="Sales by Product Category")
    pie_fig = px.pie(df, values='total_sales', names='product_category', title="Sales Distribution")

    return bar_fig, pie_fig



if __name__ == '__main__':
    app.run_server(debug=False)  # Disable debug mode in production