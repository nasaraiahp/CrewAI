# data_loader.py
import pandas as pd
import sqlite3
import os

def load_data(csv_file, db_file):
    """Loads data from a CSV file into an SQLite database."""
    try:
        # Use context manager for automatic connection closing
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            # Create table if it doesn't exist (using parameterized SQL for table creation is generally not necessary)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
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

            # Load CSV data into DataFrame
            df = pd.read_csv(csv_file)

            # Insert data into the table using executemany for efficiency
            placeholders = ', '.join(['?'] * len(df.columns))
            query = f"INSERT OR REPLACE INTO customers ({', '.join(df.columns)}) VALUES ({placeholders})"
            cursor.executemany(query, df.values.tolist())

            conn.commit()
            print(f"Data loaded successfully from {csv_file} to {db_file}")

    except Exception as e:
        print(f"Error loading data: {e}")



# Example Usage
csv_filepath = 'customer_data.csv'  # Replace with your CSV file path
db_filepath = 'customer_database.db' # Replace with your desired database file path

# Check if the database file exists, delete if it does to avoid appending data
if os.path.exists(db_filepath):
    os.remove(db_filepath)

load_data(csv_filepath, db_filepath)




# app.py (Dash app)
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

app = dash.Dash(__name__)

# Database connection (using a context manager is best practice for closing)
db_filepath = 'customer_database.db'  # Use the same database file as in data_loader.py


# Layout of the dashboard
app.layout = html.Div([
    html.H1("Customer Sales Dashboard"),

    dcc.Dropdown(
        id='country-dropdown',
        options=[], # Initialize as empty, populate in callback
        value=None,
        placeholder="Select a Country",
        multi=True
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='pie-chart')
])



# Callback to populate dropdown and initialize charts
@app.callback(
    [Output('country-dropdown', 'options'),
     Output('bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('pie-chart', 'figure')],
    Input('country-dropdown', 'value')  # This input triggers initial load
)
def initial_load(selected_countries):
    with sqlite3.connect(db_filepath) as conn:  # Context manager for connection

        country_options = [{'label': i, 'value': i} for i in pd.read_sql_query("SELECT DISTINCT Country FROM customers", conn)['Country'].unique()]
        ctx = dash.callback_context
        if not ctx.triggered: # Initial load
           selected_countries=None
        return country_options, update_bar_chart(selected_countries), update_line_chart(selected_countries), update_pie_chart(selected_countries)

# Callback functions for chart updates (bar, line, pie) - simplified
def update_bar_chart(selected_countries):
    with sqlite3.connect(db_filepath) as conn:
        query = "SELECT Country, COUNT(*) AS CustomerCount FROM customers"
        if selected_countries:
          query += f" WHERE Country IN ({', '.join(['?']*len(selected_countries))})"
        df = pd.read_sql_query(query, conn, params=selected_countries or None)
        return px.bar(df, x='Country', y='CustomerCount', title='Customer Count by Country')

def update_line_chart(selected_countries):
    with sqlite3.connect(db_filepath) as conn:
       query = "SELECT SubscriptionDate, COUNT(*) AS SubscriptionCount FROM customers"
       if selected_countries:
          query += f" WHERE Country IN ({', '.join(['?'] * len(selected_countries))})"
       query+= " GROUP BY SubscriptionDate"


       df = pd.read_sql_query(query, conn, params=selected_countries or None)
       df['SubscriptionDate'] = pd.to_datetime(df['SubscriptionDate'], errors='coerce') # Handle parsing errors
       return px.line(df, x='SubscriptionDate', y='SubscriptionCount', title='Subscription Count Over Time')


def update_pie_chart(selected_countries):
    with sqlite3.connect(db_filepath) as conn:
       query = "SELECT City, COUNT(*) AS CustomerCount FROM customers"
       if selected_countries:
          query +=  f" WHERE Country IN ({', '.join(['?']*len(selected_countries))})"
       query += " GROUP BY City"
       df = pd.read_sql_query(query, conn, params=selected_countries or None)
       return px.pie(df, values='CustomerCount', names='City', title='Customer Distribution by City')


if __name__ == '__main__':
    app.run_server(debug=True)