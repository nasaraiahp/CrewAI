# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import os

# Database setup (using a separate function for better organization)
def setup_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            category TEXT,
            sales_quantity INTEGER,
            sales_amount REAL
        )
    ''')

    dummy_data = [
        ('Product A', 'Electronics', 100, 5000),
        ('Product B', 'Clothing', 50, 2500),
        ('Product C', 'Electronics', 75, 3750),
        ('Product D', 'Clothing', 120, 6000),
        ('Product E', 'Books', 200, 4000),
        ('Product F', 'Books', 80, 1600),
    ]

    cursor.executemany("INSERT OR IGNORE INTO sales VALUES (?, ?, ?, ?)", dummy_data)
    conn.commit()
    conn.close()  # Close the connection after setup
    return db_path


# ---  Configuration and Database ---
DATABASE_PATH = os.path.join(os.getcwd(), 'sales_data.db')  # More robust path handling
setup_database(DATABASE_PATH)  # Call the database setup function


# --- Dash App ---
app = dash.Dash(__name__)

# Data Loading (outside the layout for efficiency – only loads once)
conn = sqlite3.connect(DATABASE_PATH) # Connect once per app instance
df = pd.read_sql_query("SELECT * FROM sales", conn)
conn.close()  # Important to close connection once you got data
available_categories = df['category'].unique()

app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': i, 'value': i} for i in available_categories],
        value=available_categories[0],  # Set a default value
        clearable=False  # Prevent clearing the selection
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
])


@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('category-dropdown', 'value')
)
def update_charts(selected_category):
    filtered_df = df[df['category'] == selected_category]  # df is pre-loaded now

    bar_fig = px.bar(filtered_df, x='product', y='sales_quantity', title=f'Sales Quantity by Product (Category: {selected_category})')
    pie_fig = px.pie(filtered_df, values='sales_amount', names='product', title=f'Sales Amount by Product (Category: {selected_category})')

    return bar_fig, pie_fig


if __name__ == '__main__':
    app.run_server(debug=True)