# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import sqlite3
import pandas as pd

app = dash.Dash(__name__)

# Database setup (using a temporary in-memory database for better security in this example)
conn = sqlite3.connect(':memory:')  # Use an in-memory database for demonstration
# For a persistent database, use a file path: conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        region TEXT,
        product TEXT,
        sales_amount REAL
    )
''')

# Dummy data (replace with your actual data loading logic)
dummy_data = [
    ('North', 'Product A', 1200),
    ('North', 'Product B', 850),
    ('South', 'Product A', 1500),
    ('South', 'Product C', 1000),
    ('East', 'Product B', 900),
    ('East', 'Product C', 1100),
    ('West', 'Product A', 1800),
    ('West', 'Product D', 700),
]
cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
conn.commit()


app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),

    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in pd.read_sql_query("SELECT DISTINCT region FROM sales", conn)['region'].unique()],
            value=[],  # Initialize with an empty list for multi-select
            multi=True
        )
    ]),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')

])

@app.callback(
    [Output('bar-chart', 'figure'), Output('pie-chart', 'figure')],
    [Input('region-dropdown', 'value')]
)
def update_charts(selected_regions):
    if selected_regions:  # Handle the case where no region is selected
        query = "SELECT * FROM sales WHERE region IN ({})".format(','.join('?' * len(selected_regions)))
        df = pd.read_sql_query(query, conn, params=selected_regions)
    else:
        df = pd.read_sql_query("SELECT * FROM sales", conn)  # Query all data if no selection


    bar_fig = px.bar(df, x='product', y='sales_amount', color='region', 
                     title="Sales by Product and Region")

    pie_fig = px.pie(df, values='sales_amount', names='region', 
                     title="Sales Distribution by Region")


    return bar_fig, pie_chart

if __name__ == '__main__':
    app.run_server(debug=True)