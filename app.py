# data_loader.py
import pandas as pd
import sqlite3
import os

def load_csv_to_sqlite(csv_file, db_file, table_name):
    """Loads data from a CSV file into an SQLite database table."""
    try:
        # Use context manager for automatic connection closing
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            # Parameterized query to prevent SQL injection (though less crucial for table creation)
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    Index1 INTEGER PRIMARY KEY AUTOINCREMENT,
                    CustomerID INTEGER,
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

            df = pd.read_csv(csv_file)
            df.to_sql(table_name, conn, if_exists='append', index=False)  # Default to 'append' unless replacement is specifically needed

            conn.commit()  # Commit within the context manager
            print(f"Data from '{csv_file}' loaded successfully into table '{table_name}'.")

    except Exception as e:
        print(f"Error loading data: {e}")


# Example usage – best practice to avoid running on import unless it's a module's intended purpose
if __name__ == "__main__":
    csv_filepath = 'your_data.csv'  
    db_filepath = 'sales_data.db'
    table_name = 'sales'

    # Check if the database file exists, create it if not:
    if not os.path.exists(db_filepath):
       open(db_filepath, 'w').close()


    load_csv_to_sqlite(csv_filepath, db_filepath, table_name)



# app.py (Dash app)
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

app = dash.Dash(__name__)

# Database connection configuration (improve security by NOT hardcoding in main app file)
DB_FILE = 'sales_data.db'

# Function to get database connection (handles potential errors)
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Callback to update charts
@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_charts(selected_country):

    conn = get_db_connection()
    if not conn:  # Handle database errors
        return dash.no_update, dash.no_update # Return no_update to prevent callbacks from crashing
    

    # Parameterized query to prevent SQL injection vulnerabilities
    sql_query = "SELECT * FROM sales WHERE Country = ? OR ? IS NULL"
    params = (selected_country, selected_country)

    filtered_df = pd.read_sql_query(sql_query, conn, params=params)
    conn.close() # Important to close the connection in the callback 

    # Create charts
    bar_fig = px.bar(filtered_df, x='City', y='CustomerID', title='Customers by City')
    pie_fig = px.pie(filtered_df, names='Country', title='Customer Distribution by Country')

    return bar_fig, pie_fig



# Get initial dropdown options outside the layout definition for efficiency
conn = get_db_connection()
if conn:
    df = pd.read_sql_query("SELECT DISTINCT Country FROM sales", conn)
    country_options = [{'label': i, 'value': i} for i in df['Country']]
    conn.close()
else:
    country_options = []


app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='country-dropdown',
        options=country_options,
        placeholder="Select a country",
        multi=False
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')
])



if __name__ == '__main__':
    app.run_server(debug=True)