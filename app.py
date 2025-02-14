# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# Database setup (using a context manager for better resource management)
DB_FILE = 'sales_data.db'  # Store the database filename in a variable for easier modification

def create_and_populate_db(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product_name TEXT,
            sales_amount REAL,
            region TEXT
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:
        dummy_data = [
            ('Product A', 1200, 'North'),
            ('Product B', 850, 'East'),
            ('Product C', 1500, 'West'),
            ('Product A', 900, 'South'),
            ('Product B', 1100, 'North'),
            ('Product C', 700, 'East'),
            ('Product D', 1000, 'West')
        ]
        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
        conn.commit()


# Create Dash app
app = dash.Dash(__name__)

# Prevent cross-site scripting (XSS) vulnerabilities by setting `serve_locally` to True if serving assets locally
app.config.suppress_callback_exceptions = True


# Layout of the dashboard
app.layout = html.Div([
    html.H1("Sales Dashboard"),

    dcc.Dropdown(
        id='product-dropdown',
        # The options list is populated in the callback to handle dynamic data
        value=None, # Start with no value to avoid errors on initial load. The callback will handle setting a default.
        multi=False
    ),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')
])


# Callback to update the charts and dropdown options based on data
@app.callback(
    [Output('bar-chart', 'figure'), 
     Output('pie-chart', 'figure'),
     Output('product-dropdown', 'options'),
     Output('product-dropdown', 'value')],  # Set initial dropdown value here
    [Input('product-dropdown', 'value')]
)
def update_charts(selected_product):
    with sqlite3.connect(DB_FILE) as conn: # Use a context manager for automatic closing
        create_and_populate_db(conn) # Ensure DB is created and populated inside the callback to avoid race conditions

        available_products = pd.read_sql_query("SELECT DISTINCT product_name FROM sales", conn)['product_name'].unique()
        dropdown_options = [{'label': product, 'value': product} for product in available_products]

        if selected_product is None: #  Handle the initial callback where no product is selected yet
            selected_product = available_products[0]  # Select the first product by default


        df = pd.read_sql_query("SELECT * FROM sales WHERE product_name = ?", conn, params=(selected_product,))

        # Bar chart
        bar_fig = px.bar(df, x='region', y='sales_amount', title=f'Sales of {selected_product} by Region')

        # Pie chart
        pie_fig = px.pie(df, values='sales_amount', names='region', title=f'Sales Distribution of {selected_product} across Regions')

    return bar_fig, pie_fig, dropdown_options, selected_product  # Return the dropdown options




if __name__ == '__main__':
    app.run_server(debug=True)