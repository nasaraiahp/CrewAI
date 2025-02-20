# app.py
import pandas as pd
import sqlite3
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Database setup
DB_PATH = os.path.join(os.getcwd(), 'sales_data.db')  # Use os.path.join for platform compatibility
CSV_FILE = os.path.join(os.getcwd(), 'sales_data.csv') # Use os.path.join for platform compatibility


def create_db_and_table():
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- Let SQLite handle ID generation
            CustomerId INTEGER,
            FirstName TEXT,
            LastName TEXT,
            Company TEXT,
            City TEXT,
            Country TEXT,
            Phone1 TEXT,
            Phone2 TEXT,
            Email TEXT,
            SubscriptionDate TEXT,  -- Consider storing as DATETIME
            Website TEXT 
        )
    ''')
    
    try:
        # Check if data already exists to avoid re-insertion
        cursor.execute("SELECT count(*) FROM sales")
        if cursor.fetchone()[0] == 0:  # Insert only if table is empty
            df = pd.read_csv(CSV_FILE)
            df.to_sql('sales', conn, if_exists='append', index=False)  # Use append if the table might have data
    except pd.errors.EmptyDataError: # Handle the case of empty CSV
        pass # or log a warning as appropriate
    except FileNotFoundError:
        print(f"CSV file not found at: {CSV_FILE}")  # Handle missing file
        return # Or raise an exception

    conn.commit()
    conn.close()



# Create the database and table initially
create_db_and_table()



# Dash app setup
app = dash.Dash(__name__)

# HTML layout
app.layout = html.Div([
    html.H1("Sales Data Dashboard"),
    dcc.Dropdown(
        id='chart-type',
        options=[{'label': i, 'value': i} for i in ['Bar Chart', 'Line Chart', 'Pie Chart']],
        value='Bar Chart',  # Default chart type
        clearable=False
    ),
    dcc.Graph(id='sales-chart')
])


# Callback to update the chart based on selected chart type
@app.callback(
    Output('sales-chart', 'figure'),
    [Input('chart-type', 'value')]
)
def update_chart(chart_type):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM sales", conn)

        # Convert 'SubscriptionDate' to datetime for better handling if appropriate:
        # df['SubscriptionDate'] = pd.to_datetime(df['SubscriptionDate'])

        if chart_type == 'Bar Chart':
            fig = px.bar(df, x='Country', y='CustomerId', title='Customer Count by Country')
        elif chart_type == 'Line Chart':
            fig = px.line(df, x='SubscriptionDate', y='CustomerId', title='Customer Subscriptions Over Time')  # Now handles datetime correctly
        elif chart_type == 'Pie Chart':
            fig = px.pie(df, names='Country', values='CustomerId', title='Customer Distribution by Country')
        else: 
            fig = px.bar(df, x='Country', y='CustomerId', title='Customer Count by Country')  # Default
    except pd.io.sql.DatabaseError as e:  # Catch database related errors
        print(f"Database error: {e}")
        fig = {} # or an error message figure.
    finally:
        conn.close() # ensure the connection is closed even in case of errors.
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)