# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# Database setup (better practice to separate this into a dedicated file/function)
DATABASE = 'sales_data.db'

def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            region TEXT,
            product TEXT,
            sales INTEGER
        )
    ''')

    sample_data = [
        ('North', 'Product A', 1200),
        ('North', 'Product B', 850),
        ('East', 'Product A', 1500),
        ('East', 'Product B', 1100),
        ('South', 'Product A', 900),
        ('South', 'Product B', 700),
        ('West', 'Product A', 1000),
        ('West', 'Product B', 950),
    ]
    cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", sample_data)
    conn.commit()
    conn.close()


# Create the database if it doesn't exist.  Check first to avoid re-creating if the .db file exists.
import os
if not os.path.exists(DATABASE):
    create_database()


def get_sales_data(selected_product):
    """Retrieves sales data for a given product from the database."""
    try:  # Incorporate basic error handling
        with sqlite3.connect(DATABASE) as conn: # Use connection context manager
            df = pd.read_sql_query("SELECT * FROM sales WHERE product = ?", conn, params=(selected_product,))
        return df
    except Exception as e:  # Handle potential exceptions
        print(f"Database Error: {e}")
        return pd.DataFrame() # Return empty DataFrame on error

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard (no changes needed here)
app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),
    html.Div([
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': i, 'value': i} for i in ['Product A', 'Product B']],
            value='Product A'
        )
    ]),
    dcc.Graph(id='sales-bar-chart'),
    dcc.Graph(id='sales-pie-chart')
])

# Callbacks (now using the get_sales_data function)
@app.callback(
    Output('sales-bar-chart', 'figure'),
    Input('product-dropdown', 'value')
)
def update_bar_chart(selected_product):
    df = get_sales_data(selected_product)
    if df.empty:
        return px.bar(title=f"Error Retrieving Data for {selected_product}") # Display error message in chart
    fig = px.bar(df, x='region', y='sales', title=f'Sales of {selected_product} by Region')
    return fig

@app.callback(
    Output('sales-pie-chart', 'figure'),
    Input('product-dropdown', 'value')
)
def update_pie_chart(selected_product):
    df = get_sales_data(selected_product)
    if df.empty:
        return px.pie(title=f"Error Retrieving Data for {selected_product}") # Display error message in chart
    fig = px.pie(df, values='sales', names='region', title=f'Sales Distribution of {selected_product}')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)