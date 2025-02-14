# db_utils.py
import sqlite3

DB_NAME = 'sales_data.db'

def create_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            category TEXT,
            sales_quantity INTEGER,
            sales_amount REAL
        )
    ''')
    conn.commit()
    conn.close()

def populate_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:
        dummy_data = [
            ('Product A', 'Category 1', 100, 5000),
            ('Product B', 'Category 2', 50, 2500),
            ('Product C', 'Category 1', 75, 3750),
            ('Product D', 'Category 2', 120, 6000),
            ('Product E', 'Category 3', 90, 4500),
        ]
        conn.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", dummy_data)
        conn.commit()
    conn.close()


def get_sales_data(category):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT product, sales_quantity, sales_amount FROM sales WHERE category=?", conn, params=(category,)) #Combined query
    conn.close()
    return df

def get_categories():
    conn = sqlite3.connect(DB_NAME)
    categories = pd.read_sql_query("SELECT DISTINCT category FROM sales", conn)['category'].tolist()
    conn.close()
    return categories


# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import db_utils  # Import the database functions

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the database table and populate it with initial data
db_utils.create_table()
db_utils.populate_table()



# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Sales Dashboard'),

    # Bar chart
    dcc.Graph(id='bar-chart'),

    # Pie chart
    dcc.Graph(id='pie-chart'),

    # Dropdown for product category selection
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': i, 'value': i} for i in db_utils.get_categories()],
        value=db_utils.get_categories()[0], # Default value: first category
        clearable=False
    )

])


# Callback to update both charts
@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('category-dropdown', 'value'))
def update_charts(selected_category):
    df = db_utils.get_sales_data(selected_category)

    bar_fig = px.bar(df, x='product', y='sales_quantity', title=f'Sales Quantity by Product (Category: {selected_category})')
    pie_fig = px.pie(df, values='sales_amount', names='product', title=f'Sales Amount Distribution (Category: {selected_category})')
    return bar_fig, pie_fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)