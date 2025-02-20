# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from flask import Flask

# Initialize Flask server first
server = Flask(__name__)
# Initialize the Dash app with the server
app = dash.Dash(__name__, server=server)

# Database setup (consider moving these details to a separate config file)
DATABASE = 'mydatabase.db'

def create_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sales_data (
            region TEXT,
            product TEXT,
            sales INTEGER
        )
    ''')


def insert_data(conn):
    data = [
        ('North', 'Product A', 120),
        ('North', 'Product B', 80),
        ('South', 'Product A', 150),
        ('South', 'Product B', 100),
        ('East', 'Product A', 200),
        ('East', 'Product B', 50),
    ]
    conn.executemany("INSERT OR IGNORE INTO sales_data (region, product, sales) VALUES (?, ?, ?)", data)


def get_data(conn, selected_product):
    try:
        df = pd.read_sql_query(
            "SELECT * FROM sales_data WHERE product=?", conn, params=(selected_product,)
        )
        return df
    except Exception as e:  # More specific exception handling in production
        print(f"Database query error: {e}")
        return pd.DataFrame()  # Return empty DataFrame to handle errors gracefully


# Create and populate table on startup
with sqlite3.connect(DATABASE) as conn:
    create_table(conn)
    insert_data(conn)



# Layout of the dashboard
app.layout = html.Div([
    html.H1("Sales Dashboard"),

    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': i, 'value': i} for i in ['Product A', 'Product B']],
        value='Product A'
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')
])



# Callback to update the charts
@app.callback(
    [Output('bar-chart', 'figure'), Output('pie-chart', 'figure')],
    [Input('product-dropdown', 'value')]
)
def update_charts(selected_product):
    with sqlite3.connect(DATABASE) as conn:
        df = get_data(conn, selected_product)

    if df.empty:
        return {}, {}  # Return empty figures if data retrieval fails


    bar_fig = px.bar(df, x='region', y='sales', title=f"Sales by Region for {selected_product}")
    pie_fig = px.pie(df, values='sales', names='region', title=f"Sales Distribution for {selected_product}")
    return bar_fig, pie_fig


# Run the app using the Flask server's run method
if __name__ == '__main__':
    app.run_server(debug=True)