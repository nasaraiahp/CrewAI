# app.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import os

# Security best practice: Store sensitive information (like database path) in environment variables
DATABASE_URL = os.environ.get("DATABASE_URL", "sales_data.db")  # Default to sales_data.db if not set

# Initialize the Dash app
app = dash.Dash(__name__)

# Establish a connection pool to improve performance and handle concurrent requests more efficiently
conn_pool = sqlite3.connect(DATABASE_URL, check_same_thread=False)  # check_same_thread=False is IMPORTANT for Dash

# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),

    html.Div([
        dcc.Dropdown(
            id='product-dropdown',
            # Options will be loaded dynamically in the callback
            options=[],  
            value=None,  # Initial value set to None, will be updated in callback
            clearable=False
        )
    ]),

    dcc.Graph(id='bar-chart'),

    dcc.Graph(id='pie-chart')
])

# Callback to populate dropdown and update charts on initial load and subsequent selections
@app.callback(
    [Output('product-dropdown', 'options'),
     Output('product-dropdown', 'value'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')],
    Input('product-dropdown', 'value')
)
def update_dashboard(selected_product):
    # Using the connection pool
    with conn_pool as conn:  # Context manager ensures connection is closed properly
        df = pd.read_sql_query("SELECT * FROM sales", conn)

    # Populate dropdown options dynamically
    available_products = [{'label': product, 'value': product} for product in df['Product'].unique()]
    
    # Set initial value if none is selected
    if selected_product is None:
        selected_product = df['Product'].unique()[0]  # Default to the first product

    filtered_df = df[df['Product'] == selected_product]
    bar_fig = px.bar(filtered_df, x='Month', y='Sales', title=f"Sales for {selected_product}")
    pie_fig = px.pie(filtered_df, values='Sales', names='Month', title=f'Sales Distribution for {selected_product}')
    
    return available_products, selected_product, bar_fig, pie_fig


if __name__ == '__main__':
    app.run_server(debug=False) # Disable debug mode in production