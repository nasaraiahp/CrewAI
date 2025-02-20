import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import sqlite3
import pandas as pd

# --- Database Interactions ---
# Use a context manager for database connections to ensure proper closing
# and handle potential exceptions.

def get_db_connection():
    return sqlite3.connect('sales_data.db')

def create_sales_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            category TEXT,
            sales_amount REAL
        )
    ''')

def insert_dummy_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:
        dummy_data = [
            ('Product A', 'Category 1', 1200),
            ('Product B', 'Category 2', 850),
            ('Product C', 'Category 1', 1500),
            ('Product D', 'Category 3', 1000),
            ('Product E', 'Category 2', 900),
        ]
        conn.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
        conn.commit()

# Initialize database on app startup
with get_db_connection() as conn:
    create_sales_table(conn)
    insert_dummy_data(conn)


# --- Dash App ---
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),

    dcc.Graph(id='sales-bar-chart'),

    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': 'All', 'value': 'All'}], # Initial options, updated in callback
        value='All',
        clearable=False
    ),

    dcc.Graph(id='sales-pie-chart'),

])

@app.callback(
    [Output('sales-bar-chart', 'figure'),
     Output('sales-pie-chart', 'figure'),
     Output('category-dropdown', 'options')],  # Update dropdown options dynamically
    [Input('category-dropdown', 'value')]
)
def update_charts(selected_category):
    with get_db_connection() as conn:
        if selected_category == 'All':
            df = pd.read_sql_query("SELECT * FROM sales", conn)
        else:
            # Use parameterized query to prevent SQL injection
            df = pd.read_sql_query("SELECT * FROM sales WHERE category = ?", conn, params=(selected_category,))

        # Dynamically update dropdown options.  Only make this database call once per page load.
        all_categories = pd.read_sql_query("SELECT DISTINCT category FROM sales", conn)
        dropdown_options = [{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in all_categories['category']]

    bar_fig = px.bar(df, x='product', y='sales_amount', color='category', title='Sales by Product')
    pie_fig = px.pie(df, values='sales_amount', names='product', title='Sales Distribution')

    return bar_fig, pie_fig, dropdown_options  # Return the updated dropdown options


if __name__ == '__main__':
    app.run_server(debug=True)