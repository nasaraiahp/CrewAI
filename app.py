import pandas as pd
import sqlite3
import dash
from dash import dcc, html, Input, Output
from dash.dash_table import DataTable
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask

# --- Configuration ---
DATABASE_PATH = 'sales_data.db'  # Use a constant for the database path
CSV_FILE = 'sales_data.csv'  # Use a constant for the CSV file path

# --- Data Loading and Database Interaction ---

def load_data_to_db(csv_file, db_path):
    """Loads data from a CSV file into an SQLite database.

    Args:
        csv_file (str): Path to the CSV file.
        db_path (str): Path to the SQLite database file.

    Returns:
        pandas.DataFrame or None: The DataFrame if loading is successful, None otherwise.
    """
    try:
        conn = sqlite3.connect(db_path)  # No need to explicitly close if using a context manager
        df = pd.read_csv(csv_file, parse_dates=['SubscriptionDate'])  # Parse dates on load

        with conn:  # Use a context manager to automatically commit/rollback and close the connection
            df.to_sql('sales_data', conn, if_exists='replace', index=False)
        print("Data loaded successfully!")
        return df

    except Exception as e:
        print(f"An error occurred during data loading: {e}")
        return None

# --- Dash App ---
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True) # Suppress callback exceptions

df = load_data_to_db(CSV_FILE, DATABASE_PATH)

if df is not None:
    app.layout = html.Div([
        html.H1("Sales Dashboard"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['Country'].unique()],
            value=df['Country'].iloc[0] if not df['Country'].empty else None,  # Handle potential empty DataFrame
            multi=False,
            clearable=False #Prevent clearing the selection entirely, ensuring there's always a value for the callbacks
        ),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='line-chart'),
        dcc.Graph(id='pie-chart')
    ])


    @app.callback(
        [Output('bar-chart', 'figure'),
         Output('line-chart', 'figure'),
         Output('pie-chart', 'figure')],
        Input('country-dropdown', 'value')
    )
    def update_charts(selected_country):
        filtered_df = df[df['Country'] == selected_country]


        bar_fig = px.bar(filtered_df, x='City', title=f'Customers per City ({selected_country})')

        line_fig = px.line(filtered_df, x='SubscriptionDate', y='CustomerId',
                           title=f'Subscriptions Over Time ({selected_country})')

        pie_fig = px.pie(filtered_df, values='CustomerId', names='Company',
                         title=f'Customer Distribution by Company ({selected_country})')

        return bar_fig, line_fig, pie_fig


    if __name__ == '__main__':
        app.run_server(debug=True)