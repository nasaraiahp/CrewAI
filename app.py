# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import os

# Database setup (best practice to externalize configuration)
DATABASE_URL = os.environ.get("DATABASE_URL", "sales_data.db")  # Use environment variable for Heroku

# Create a connection function for reusability and better resource management
def get_db_connection():
    return sqlite3.connect(DATABASE_URL)

# Initialize database if it doesn't exist (check outside the main app logic)
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            sales_quantity INTEGER,
            sales_region TEXT
        )
    ''')

    # Check if table is empty before inserting sample data. This prevents duplicates on each run.
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0: # Check if the table is empty. If it is, then populate table.
        sample_data = [
            ('Product A', 100, 'North America'),
            ('Product B', 150, 'Europe'),
            ('Product C', 200, 'Asia'),
            ('Product A', 75, 'Europe'),
            ('Product B', 120, 'North America'),
            ('Product C', 180, 'Asia'),
            ('Product D', 90, 'North America'),
            ('Product E', 110, 'Europe')
        ]
        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", sample_data)
        conn.commit()



app = dash.Dash(__name__)
server = app.server  # For gunicorn/heroku deployment

app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),

    html.Div([
        html.Label("Select Sales Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': i, 'value': i} for i in ['All', 'North America', 'Europe', 'Asia']],
            value='All'
        )
    ], style={'width': '30%', 'display': 'inline-block'}),

    dcc.Graph(id='sales-bar-chart'),
    dcc.Graph(id='sales-pie-chart')
])


@app.callback(
    [Output('sales-bar-chart', 'figure'),
     Output('sales-pie-chart', 'figure')],
    [Input('region-dropdown', 'value')]
)
def update_charts(selected_region):
    with get_db_connection() as conn:  # Context manager ensures connection is closed
        df = pd.read_sql_query("SELECT * FROM sales", conn)
        
    if selected_region != 'All':
        df = df[df['sales_region'] == selected_region]

    bar_fig = px.bar(df, x='product', y='sales_quantity', title="Sales by Product")
    pie_fig = px.pie(df, values='sales_quantity', names='product', title='Sales Distribution by Product')

    return bar_fig, pie_fig



if __name__ == '__main__':
    app.run_server(debug=True)