# data_loader.py
import pandas as pd
import sqlite3
import os

def load_csv_to_sqlite(csv_filepath, db_filepath, table_name):
    """Loads data from a CSV file into an SQLite database table.

    Args:
        csv_filepath: Path to the CSV file.
        db_filepath: Path to the SQLite database file.
        table_name: Name of the table to create or insert into.
    """
    try:
        # Check if the CSV file exists
        if not os.path.exists(csv_filepath):
            raise FileNotFoundError(f"CSV file not found: {csv_filepath}")

        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(csv_filepath)

        # Use a context manager for the database connection
        with sqlite3.connect(db_filepath) as conn:
            # Create a cursor object
            cursor = conn.cursor()

            # Use parameterized SQL to prevent SQL injection vulnerabilities
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    CustomerId INTEGER,
                    FirstName TEXT,
                    LastName TEXT,
                    Company TEXT,
                    City TEXT,
                    Country TEXT,
                    Phone1 TEXT,
                    Phone2 TEXT,
                    Email TEXT,
                    SubscriptionDate TEXT,
                    Website TEXT
                )
            ''')


            # Insert data using executemany for efficiency
            placeholders = ','.join(['?'] * len(df.columns))
            insert_sql = f"INSERT OR IGNORE INTO {table_name} ({','.join(df.columns)}) VALUES ({placeholders})" # Use INSERT OR IGNORE to handle potential duplicates
            cursor.executemany(insert_sql, df.values.tolist())


            # Commit is handled automatically by the context manager

        print(f"Data from '{csv_filepath}' loaded successfully into '{table_name}' table in '{db_filepath}'")

    except Exception as e:
        print(f"An error occurred: {e}")



# Example usage
load_csv_to_sqlite('customer_data.csv', 'sales_data.db', 'customers')



# app.py (Dash app)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

app = dash.Dash(__name__)

# Database filepath (consistent with data_loader.py)
DB_FILEPATH = 'sales_data.db'

# Layout
app.layout = html.Div([
    html.H1("Sales Data Dashboard"),
    dcc.Dropdown(
        id='chart-type',
        options=[{'label': 'Bar Chart', 'value': 'bar'},
                 {'label': 'Line Chart', 'value': 'line'},
                 {'label': 'Pie Chart', 'value': 'pie'}],
        value='bar'
    ),
    dcc.Graph(id='sales-chart'),
])

# Callback
@app.callback(
    Output('sales-chart', 'figure'),
    Input('chart-type', 'value')
)
def update_chart(chart_type):
    # Use a context manager for database connections within the callback
    with sqlite3.connect(DB_FILEPATH) as conn:
        # Use pandas.read_sql_query for simpler database interaction
        df = pd.read_sql_query(
            "SELECT Country, COUNT(*) AS CustomerCount FROM customers GROUP BY Country", conn
        )

    fig = {}  # Initialize fig
    if df.empty:
        return fig  # Handle empty DataFrame


    if chart_type == 'bar':
        fig = px.bar(df, x='Country', y='CustomerCount', title='Customer Count by Country')
    elif chart_type == 'line':
        fig = px.line(df, x='Country', y='CustomerCount', title='Customer Count by Country')
    elif chart_type == 'pie':
        fig = px.pie(df, values='CustomerCount', names='Country', title='Customer Distribution by Country')

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)