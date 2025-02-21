import pandas as pd
import sqlite3
from dash import Dash, html, dcc
import plotly.express as px
from flask import Flask
import os

# --- Configuration ---
DATABASE_PATH = os.path.join(os.getcwd(), 'sales_data.db')  # Use os.path.join for platform compatibility
CSV_PATH = 'your_data.csv'  # Store CSV path separately
DEBUG_MODE = os.environ.get("DEBUG_MODE", "False").lower() == "true" # Get debug mode from environment variable

# --- Data Loading and Database Interaction ---
def create_and_populate_db(db_path, csv_path):
    """Creates the database table and populates it with data from the CSV."""
    try:
        with sqlite3.connect(db_path) as conn:  # Use context manager for automatic connection closing
            cursor = conn.cursor()

            create_table_query = """
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
            """
            cursor.execute(create_table_query)

            try:
                df = pd.read_csv(csv_path)
                df.to_sql('customers', conn, if_exists='replace', index=False)
            except FileNotFoundError:
                print(f"CSV file not found at {csv_path}. Database table created but not populated.")
                return False # Indicate that CSV loading failed

        return True

    except Exception as e:
        print(f"An error occurred during database operations: {e}")
        return False

# Create and populate the database
if create_and_populate_db(DATABASE_PATH, CSV_PATH):
    print("Database successfully created and populated.")
else:
    print("Database creation or population encountered an issue.")


# --- Dash/Flask App ---
server = Flask(__name__)
app = Dash(__name__, server=server)

# Data Query Function (for better organization and reusability)
def query_data(db_path, query="SELECT * FROM customers"):
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query, conn)
    return df

df = query_data(DATABASE_PATH) # Query data only after successful database creation


# Dashboard Layout
app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),

    # ... (Graphs remain the same, but consider adding error handling if df is empty) 

])

if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE)  # Use environment variable for debug mode