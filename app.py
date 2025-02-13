# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from flask_caching import Cache

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Configure caching (adjust config as needed)
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

# Database setup (using a context manager for better resource management)
DATABASE = 'sales_data.db'  # Store database name as a constant

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Use row factory for dictionary-like access
    return conn

def create_table_if_not_exists():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                region TEXT,
                product TEXT,
                sales REAL
            )
        ''')
        # Populate with dummy data if table is empty (using a transaction)
        cursor.execute("SELECT COUNT(*) FROM sales")
        if cursor.fetchone()[0] == 0:
            dummy_data = [
                ('North', 'Product A', 1000),
                ('North', 'Product B', 1500),
                ('South', 'Product A', 800),
                ('South', 'Product B', 1200),
                ('East', 'Product A', 1200),
                ('East', 'Product B', 900),
                ('West', 'Product A', 700),
                ('West', 'Product B', 1100),
            ]
            cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
            conn.commit()  # Commit after inserts

# Call the function to create the table if it doesn't exist
create_table_if_not_exists()



@cache.memoize(timeout=60)  # Cache data for 60 seconds
def query_data(selected_regions):
    with get_db_connection() as conn:
        if not selected_regions:
            df = pd.read_sql_query("SELECT * FROM sales", conn)
        else: 
            df = pd.read_sql_query(f"SELECT * FROM sales WHERE region IN ({','.join('?'*len(selected_regions))})", conn, params=selected_regions)

        return df



# Layout of the dashboard
app.layout = html.Div([
    html.H1("Sales Dashboard"),
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': i['region'], 'value': i['region']} for i in get_db_connection().execute("SELECT DISTINCT region FROM sales").fetchall()],  # Improve dropdown creation with list comprehension
            value=[], # Allow for no initial value by starting with an empty list
            multi=True
        )
    ]),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')
])



# Callback to update charts based on region selection
@app.callback(
    [Output('bar-chart', 'figure'), Output('pie-chart', 'figure')],
    [Input('region-dropdown', 'value')]
)
def update_charts(selected_regions):

    df = query_data(selected_regions)

    bar_chart = px.bar(df, x='product', y='sales', color='region', barmode='group', title="Sales by Product and Region")
    pie_chart = px.pie(df, values='sales', names='region', title="Sales Distribution by Region")
    return bar_chart, pie_chart

if __name__ == '__main__':
    app.run_server(debug=True)