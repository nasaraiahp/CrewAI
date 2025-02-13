# app.py
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import sqlite3
import os

# Database setup (Best practice: separate database interactions into a function)
DATABASE_PATH = os.path.join(os.getcwd(), 'sales_data.db')  # Store the database in the current working directory

def create_and_populate_db(db_path=DATABASE_PATH):
    """Creates and populates the database if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product_name TEXT,
            sales_amount REAL,
            sales_region TEXT
        )
    ''')
    # Check if table is empty before inserting default data (avoids duplicate entries on every run)
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:  # Insert data if table is empty
        sample_data = [
            ('Product A', 1500, 'North'),
            ('Product B', 2200, 'East'),
            ('Product C', 1800, 'West'),
            ('Product A', 1200, 'South'),
        ]
        cursor.executemany("INSERT INTO sales (product_name, sales_amount, sales_region) VALUES (?, ?, ?)", sample_data)
        conn.commit()
    conn.close()


# Call this function once at app startup to ensure db exists and has the initial sample data if empty
create_and_populate_db()

# Dash app setup
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

# Layout
app.layout = html.Div([
    html.H1("Sales Dashboard"),

    html.Div([
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': i, 'value': i} for i in ['All'] + ['Product A', 'Product B', 'Product C']], # Get these from db ideally
            value='All',
            clearable=False,
        ),
        dcc.Graph(id='bar-chart'),
    ]),

    html.Div([
        dcc.Graph(id='pie-chart'),
    ])
])

# Callbacks
@app.callback(
    [Output('bar-chart', 'figure'), Output('pie-chart', 'figure')],
    Input('product-dropdown', 'value')
)
def update_charts(selected_product):
    conn = sqlite3.connect(DATABASE_PATH)  # Use the constant
    try:
        df = pd.read_sql_query("SELECT * FROM sales", conn)
    finally:
        conn.close()  # Always close the connection in a finally block

    if selected_product != 'All':
        df = df[df['product_name'] == selected_product]

    bar_fig = px.bar(df, x='sales_region', y='sales_amount', color="product_name", title="Sales by Region")
    pie_fig = px.pie(df, values='sales_amount', names='product_name', title="Sales Distribution by Product")
    return bar_fig, pie_fig


if __name__ == '__main__':
    app.run_server(debug=True)