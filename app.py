# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import sqlite3
import pandas as pd  # Import pandas explicitly
import os

# Database setup (better practice to separate this)
DB_PATH = os.path.join(os.getcwd(), 'sales_data.db')  # Use os.path.join

def create_and_populate_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            category TEXT,
            sales_amount REAL
        )
    ''')
    # Use parameterized queries to prevent SQL injection (even with sample data)
    data = [('Product A', 'Category 1', 1500),
            ('Product B', 'Category 2', 2200),
            ('Product C', 'Category 1', 1800),
            ('Product D', 'Category 2', 1200)]
    cursor.executemany("INSERT OR IGNORE INTO sales (product, category, sales_amount) VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()

# Create and populate the database if it doesn't exist
if not os.path.exists(DB_PATH): # check if database exists
    create_and_populate_db()




app = dash.Dash(__name__)
server = app.server # This line is added to allow for deployment on platforms like Heroku


app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='chart-type',
        options=[
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Pie Chart', 'value': 'pie'}
        ],
        value='bar',
        style={'width': '300px'}
    ),
    dcc.Graph(id='sales-chart'),

])


@app.callback(
    Output('sales-chart', 'figure'),
    Input('chart-type', 'value')
)
def update_chart(chart_type):

    conn = sqlite3.connect(DB_PATH) # consistent use of db path
    try:
        df = pd.read_sql_query("SELECT * from sales", conn)
    finally:
        conn.close() # Ensure connection closes even if error

    if chart_type == 'bar':
        fig = px.bar(df, x='product', y='sales_amount', color='category', 
                     title="Sales by Product and Category")
    elif chart_type == 'pie':
        fig = px.pie(df, values='sales_amount', names='category', title="Sales Distribution by Category")
    else:
        fig = {} # Return an empty figure as default

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)