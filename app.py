# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# Database setup (consider moving to a separate file for larger applications)
DATABASE = 'sales_data.db'

def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            category TEXT,
            sales_amount REAL
        )
    ''')

    dummy_data = [
        ('Product A', 'Category 1', 1200),
        ('Product B', 'Category 1', 850),
        ('Product C', 'Category 2', 1500),
        ('Product D', 'Category 2', 1100),
        ('Product E', 'Category 3', 900),
        ('Product F', 'Category 3', 1300),
    ]
    # Check if the table is empty before inserting dummy data
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:  # Insert only if the table is empty
        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
        conn.commit()
    conn.close()


# Create the database if it doesn't exist
create_database()


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Data Dashboard"),

    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': i, 'value': i} for i in ['All'] + list(pd.read_sql_query("SELECT DISTINCT category FROM sales", sqlite3.connect(DATABASE))['category'])],  # Dynamically populate dropdown
        value='All',  # Default value
        clearable=False  # Prevent clearing the selection
    ),

    dcc.Graph(id='sales-bar-chart'),
    dcc.Graph(id='sales-pie-chart')
])


@app.callback(
    [Output('sales-bar-chart', 'figure'), Output('sales-pie-chart', 'figure')],
    Input('category-dropdown', 'value')
)
def update_charts(selected_category):
    # Use parameterized query to prevent SQL injection
    sql = "SELECT * FROM sales"
    params = ()

    if selected_category != 'All':
        sql = "SELECT * FROM sales WHERE category = ?"
        params = (selected_category,) # Make a tuple

    with sqlite3.connect(DATABASE) as conn:  # Context manager ensures connection is closed
        df = pd.read_sql_query(sql, conn, params=params)  # Use params with the query

    bar_fig = px.bar(df, x='product', y='sales_amount', color='category', title='Sales by Product')
    pie_fig = px.pie(df, values='sales_amount', names='product', title='Sales Distribution')
    return bar_fig, pie_fig



if __name__ == '__main__':
    app.run_server(debug=True)