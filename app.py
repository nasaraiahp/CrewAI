import pandas as pd
import sqlite3
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Database and CSV handling improvements
db_file = 'sales_data.db'
csv_file = 'sales_data.csv'

# Check if the database file exists; create if it doesn't
if not os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
    # Improve security by parameterizing SQL query
    # This is not relevant for the CREATE TABLE part but is shown as an example for later parts.
    conn.execute("CREATE TABLE IF NOT EXISTS sales ( --Add your column definitions here. It's good practice to define column types-- )") # Example: CREATE TABLE sales (col1 TEXT, col2 REAL...) 
    conn.close()

# Load CSV only if database is empty or doesn't have the 'sales' table

try:  # Try/Except block for more robust error handling
    conn = sqlite3.connect(db_file)
    table_exists = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'", conn).shape[0] > 0

    if not table_exists:
        print(f"Loading from '{csv_file}' into database.")
        df = pd.read_csv(csv_file)
        df.to_sql('sales', conn, if_exists='replace', index=False)

    conn.close()  # Close the connection in the `try` block after use
except Exception as e: # Handle exceptions during CSV or Database interaction
    print(f"Error during database setup or CSV import: {e}")


# Dash App Setup
app = dash.Dash(__name__)
app.title = "Sales Data Dashboard"  # Set the title for the dashboard

# Layout -  Improve structure and add user controls (example dropdown)
app.layout = html.Div([
    html.H1("Sales Data Dashboard"),

    # Add a dropdown to select country (example)
    dcc.Dropdown(id='country-dropdown',
                 options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Country'].unique()],  # Dynamic options
                 value='All',  # Default value
                 clearable=False  # User can't clear the dropdown selection
                 ),


    dcc.Graph(id='bar-chart-country'),
    dcc.Graph(id='line-chart-time'),
    dcc.Graph(id='pie-chart-customers'),
    dcc.Graph(id='bar-chart-customers'),
    dcc.Graph(id='line-chart-product'),
    dcc.Store(id='intermediate-value')  # Store to hold pre-processed data (if necessary)
])



# Callback Functions - now using the Dropdown example as Input for filtering

@app.callback(
    Output('bar-chart-country', 'figure'),
    Input('country-dropdown', 'value') # Input is country dropdown
)
def update_bar_chart_country(selected_country):
    conn = sqlite3.connect(db_file)
    if selected_country == "All":
        df = pd.read_sql_query("SELECT Country, COUNT(*) AS SalesCount FROM sales GROUP BY Country", conn)
    else:
        df = pd.read_sql_query(f"SELECT Country, COUNT(*) AS SalesCount FROM sales WHERE Country = ? GROUP BY Country", conn, params=(selected_country,)) # Parameterized query
    conn.close()
    return px.bar(df, x='Country', y='SalesCount', title="Sales by Country")


# Other callbacks... (similar adjustments for inputs and query parameters for filtering)
# ...



if __name__ == '__main__':
    app.run_server(debug=True)