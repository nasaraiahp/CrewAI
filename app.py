# app.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import os

# Database setup (best practice to separate configuration)
DATABASE_PATH = os.getenv('DATABASE_PATH', 'sales_data.db')  # Use environment variable if available

# Create a connection to the SQLite database (using a context manager for safe closing)
def get_db_connection():
    return sqlite3.connect(DATABASE_PATH)

# Data loading and initialization (perform this only once)
with get_db_connection() as conn:
    # Sample sales data (in real application, load from an external source like CSV)
    sales_data = {
        'Product': ['A', 'B', 'C', 'D', 'E'],
        'Sales': [1200, 850, 1500, 1000, 900],
        'Region': ['North', 'South', 'East', 'West', 'North']
    }

    df = pd.DataFrame(sales_data)

    # Store the DataFrame in the SQLite database (only if it doesn't exist)
    df.to_sql('sales', conn, if_exists='replace', index=False)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Dashboard"),

    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[], # Options will be loaded dynamically
            value=[],  # Initially, no region selected (list for multi-select)
            multi=True, 
            placeholder="All Regions"
        ),
    ]),

    dcc.Graph(id='sales-bar-chart'),
    dcc.Graph(id='sales-pie-chart')
])

@app.callback(
    Output('region-dropdown', 'options'),
    Input('region-dropdown', 'value') # Not used, but ensures the callback is triggered on startup
)
def load_region_options(_):  # _ as the input is not actually used
    with get_db_connection() as conn:
        region_options = pd.read_sql_query("SELECT DISTINCT Region FROM sales", conn)['Region'].tolist()
        return [{'label': region, 'value': region} for region in region_options]


@app.callback(
    [Output('sales-bar-chart', 'figure'),
     Output('sales-pie-chart', 'figure')],
    [Input('region-dropdown', 'value')]
)
def update_charts(selected_regions):
    with get_db_connection() as conn:
        if selected_regions:
            query = "SELECT * FROM sales WHERE Region IN ({})".format(','.join(['?'] * len(selected_regions)))
            filtered_df = pd.read_sql_query(query, conn, params=selected_regions)
        else:
            filtered_df = pd.read_sql_query("SELECT * FROM sales", conn)

    bar_fig = px.bar(filtered_df, x='Product', y='Sales', title='Sales by Product')
    pie_fig = px.pie(filtered_df, values='Sales', names='Product', title='Sales Distribution')

    return bar_fig, pie_fig


if __name__ == '__main__':
    app.run_server(debug=True)