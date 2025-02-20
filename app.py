# app.py
import pandas as pd
import sqlite3
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Database and CSV configuration (using environment variables for better security)
DB_PATH = os.environ.get("SALES_DB_PATH", "sales_data.db")  # Use environment variable or default
CSV_FILE_PATH = os.environ.get("SALES_CSV_PATH", "sales_data.csv")

# Dash app setup
app = dash.Dash(__name__)
app.title = "Sales Data Dashboard"  # Set the title for the browser tab

# --- Data Loading and Preprocessing ---
try:
    # Use a context manager for database connection
    with sqlite3.connect(DB_PATH) as conn:
        # Check if the table exists before reading the CSV (for efficiency)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
        table_exists = cursor.fetchone()

        if not table_exists:  # Only read and insert if the table doesn't exist
            df = pd.read_csv(CSV_FILE_PATH, parse_dates=["SubscriptionDate"])  # Parse dates directly

            df.to_sql('sales', conn, if_exists='replace', index=False)

        # Read data from the database (after potentially creating it)
        df = pd.read_sql_query("SELECT * FROM sales", conn)



except Exception as e:
    print(f"An error occurred during data loading: {e}")
    # Consider a more robust error handling strategy (e.g., logging, exit)
    exit(1)  # Exit if data loading fails



# --- Layout ---
app.layout = html.Div([
    html.H1("Sales Data Dashboard"),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Country'].unique()],
        value=None,
        placeholder="Select a Country",
        clearable=True,  # Allow clearing the selection
    ),
    dash_table.DataTable(
        id='sales-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        page_size=10,
        style_table={'overflowX': 'auto'}  # Horizontal scrolling for wide tables

    ),
    dcc.Graph(id='sales-graph'),
])


# --- Callbacks ---
@app.callback(
    Output('sales-graph', 'figure'),
    Input('country-dropdown', 'value')
)
def update_graph(selected_country):
    filtered_df = df if selected_country is None else df[df['Country'] == selected_country]
    fig = px.histogram(filtered_df, x='SubscriptionDate', title="Subscription Distribution")
    return fig



# --- Run the app ---
if __name__ == '__main__':
    app.run_server(debug=True)