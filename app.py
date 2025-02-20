# app.py
import pandas as pd
import sqlite3
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Database configuration
DATABASE_PATH = os.path.join(os.getcwd(), 'sales_data.db')  # Use os.path.join for platform compatibility

# SQL queries parameterized for security
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS sales (
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
);
"""

INSERT_DATA_QUERY = "INSERT INTO sales VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"


def load_data(conn, csv_path):
    try:
        df = pd.read_csv(csv_path)
        df['SubscriptionDate'] = pd.to_datetime(df['SubscriptionDate'])  # Convert to datetime on load
        df.to_sql('sales', conn, if_exists='replace', index=False)
    except FileNotFoundError:
        print(f"CSV file not found at: {csv_path}")  # More specific error message.
        exit(1)  # Use a non-zero exit code to indicate an error
    except Exception as e:  # Catch more general exceptions
        print(f"An error occurred loading data: {e}")
        exit(1)

# Establish database connection and load data
try:
    conn = sqlite3.connect(DATABASE_PATH)  # Use parameterized path

    # Use parameterized query to create the table
    conn.execute(CREATE_TABLE_QUERY)

    # Load data only if a CSV path is provided
    csv_file_path = os.getenv('CSV_FILE_PATH')  # Use environment variables to provide the path

    if csv_file_path:
        load_data(conn, csv_file_path)
    else:
        print("Warning: No CSV file path provided. Using existing database or starting with an empty one.")



except Exception as e:
    print(f"Database error: {e}")
    exit(1)


# Create Dash app
app = Dash(__name__)

# App layout (no changes here for now)
# ... (same layout as before)


# Callback functions (mostly the same logic)
# ... (callbacks with minor changes as detailed below)



# ... (Rest of the callbacks are the same, except update_subscription_trend, see below)

def update_subscription_trend():
    # Use a parameterized query to fetch data
    query = "SELECT SubscriptionDate, COUNT(CustomerId) AS CustomerCount FROM sales GROUP BY SubscriptionDate"
    subscriptions_over_time = pd.read_sql_query(query, conn, parse_dates=['SubscriptionDate'])

    subscriptions_over_time = subscriptions_over_time.groupby(subscriptions_over_time['SubscriptionDate'].dt.to_period('M'))['CustomerCount'].sum().reset_index()
    subscriptions_over_time['SubscriptionDate'] = subscriptions_over_time['SubscriptionDate'].dt.to_timestamp()
    fig = px.line(subscriptions_over_time, x='SubscriptionDate', y='CustomerCount', title='Trend of New Subscriptions Over Time')
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)  # Disable debug mode in production