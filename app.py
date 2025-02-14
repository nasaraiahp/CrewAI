# app.py (Python)
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import os

# Database setup (better practice to separate this if it grows complex)
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'sales_data.db')  # Use os.path.join

def create_and_populate_db(db_path=DATABASE_PATH):  # Function to create and populate
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            category TEXT,
            sales_value REAL
        )
    ''')

    dummy_data = [
        ('Product A', 'Electronics', 1200),
        ('Product B', 'Clothing', 850),
        ('Product C', 'Electronics', 1500),
        ('Product D', 'Books', 600),
        ('Product E', 'Clothing', 900),
        ('Product F', 'Electronics', 1100),
        ('Product G', 'Books', 700),
        ('Product H', 'Clothing', 1000)
    ]
    cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
    conn.commit()
    conn.close()


# Create the database if it doesn't exist.  Good for initial setup.
if not os.path.exists(DATABASE_PATH): 
    create_and_populate_db()



app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),

    dcc.Dropdown(
        id='category-filter',
        options=[{'label': i, 'value': i} for i in ['All'] + ['Electronics', 'Clothing', 'Books']],
        value='All',
        clearable=False
    ),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')

])


@app.callback(
    [Output('bar-chart', 'figure'), Output('pie-chart', 'figure')],
    [Input('category-filter', 'value')]
)
def update_charts(selected_category):
    conn = sqlite3.connect(DATABASE_PATH)  # Use DATABASE_PATH
    try:
        df = pd.read_sql_query("SELECT * FROM sales", conn)  # Keep connection open only while necessary
    finally:
        conn.close() # Ensure the connection is ALWAYS closed, even if errors occur.

    if selected_category != 'All':
        df = df[df['category'] == selected_category]

    bar_fig = px.bar(df, x='product', y='sales_value', color='category',
                     title=f'Sales by Product ({selected_category if selected_category != "All" else "All Categories"})')
    pie_fig = px.pie(df, values='sales_value', names='category',
                     title=f'Sales Distribution by Category ({selected_category if selected_category != "All" else "All Categories"})')

    return bar_fig, pie_fig



if __name__ == '__main__':
    app.run_server(debug=True)