# data_loader.py
import pandas as pd
import sqlite3
import os

def load_csv_to_sqlite(csv_file, db_file, table_name):
    """Loads data from a CSV file into an SQLite database."""
    try:
        # Parameterize the table name to prevent SQL injection (though less critical for table names)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Use parameterized SQL to create the table
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Let SQLite handle id generation
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


        # Load CSV data into a Pandas DataFrame
        df = pd.read_csv(csv_file)

        # Insert data using parameterized SQL for security
        placeholders = ', '.join(['?'] * len(df.columns))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"
        cursor.executemany(insert_sql, df.values.tolist())


        conn.commit()
        print(f"Data from '{csv_file}' loaded into table '{table_name}' successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()


# Example usage (ensure the CSV file exists in the same directory)
load_csv_to_sqlite("customer_data.csv", "customer_database.db", "customers")



# app.py (Dash app)
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

app = dash.Dash(__name__)

# Database details (better to store these securely, e.g., in environment variables)
DB_FILE = "customer_database.db"
TABLE_NAME = "customers"

# Load data from the database
def load_data_from_db():
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
        return df
    except Exception as e:
        print(f"Database Error: {e}")  # Handle potential database errors
        return pd.DataFrame()  # Return an empty DataFrame if there's an error
    finally:
        conn.close()


df = load_data_from_db()

app.layout = html.Div([
    html.H1("Customer Data Dashboard"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Country'].unique()],
        value=[],  # Initialize with an empty list for multi-select
        multi=True,
        placeholder="Select Country/Countries"

    ),
    dcc.Graph(id='sales-graph')
])



@app.callback(
    Output('sales-graph', 'figure'),
    Input('country-dropdown', 'value')
)
def update_graph(selected_countries):
    if not selected_countries:  # Check if the list is empty
        filtered_df = df
    else:
        filtered_df = df[df['Country'].isin(selected_countries)]

    fig = px.histogram(filtered_df, x='Country', title='Customer Count by Country')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)  # Specify port for clarity