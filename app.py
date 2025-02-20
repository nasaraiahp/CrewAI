# app.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from pathlib import Path

# Database setup (using a file path that works across systems)
DB_FILE = Path(__file__).parent / "sales_data.db"  # Store in the same directory as the script
DB_CONNECTION_STRING = f"sqlite:///{DB_FILE}"


def create_and_populate_db(db_path):
    """Creates the database and populates it with dummy data if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            category TEXT,
            sales_amount REAL
        )
    ''')

    # Check if the table is empty before inserting dummy data
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:  # Insert only if the table is empty
        dummy_data = [
            ('Product A', 'Electronics', 1500),
            ('Product B', 'Clothing', 1200),
            ('Product C', 'Electronics', 1800),
            ('Product D', 'Books', 800),
            ('Product E', 'Clothing', 1000),
            ('Product F', 'Books', 900),
            ('Product G', 'Electronics', 2200),
            ('Product H', 'Clothing', 1500),
        ]
        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
        conn.commit()

    conn.close()

# Ensure the database file and dummy data exists
create_and_populate_db(DB_FILE)



app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
    dcc.Dropdown(
        id='product-dropdown',
        options=[], # Options will be loaded dynamically
        value=[], # Default value as a list since multi=True
        multi=True,
        placeholder="Select Products"
    )
])

@app.callback(
    Output('product-dropdown', 'options'),
    Input('product-dropdown', 'value') # Not really used, but needed for initial loading. Dash 3.0+ has other features.
)
def update_dropdown_options(_): # Input not used but required by Dash.
    conn = sqlite3.connect(DB_FILE)  # Use the constant for consistency
    df = pd.read_sql_query("SELECT DISTINCT product FROM sales", conn)
    conn.close()

    return [{'label': product, 'value': product} for product in df['product'].tolist()]



@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('product-dropdown', 'value')
)
def update_charts(selected_products):

    # Use the more efficient read_sql with the connection string, no need to open/close within callback
    df = pd.read_sql("SELECT * FROM sales", DB_CONNECTION_STRING) 


    if selected_products: # Check if the list is not empty
        df = df[df['product'].isin(selected_products)]  # Filter data

    bar_fig = px.bar(df, x='product', y='sales_amount', color='category', title="Sales by Product and Category")
    pie_fig = px.pie(df, values='sales_amount', names='category', title="Sales Distribution by Category")

    return bar_fig, pie_fig



if __name__ == '__main__':
    app.run_server(debug=True)