# app.py
import pandas as pd
import sqlite3
import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Database setup (using environment variables for database path is recommended for security)
db_path = os.environ.get('DATABASE_URL', 'sales_data.db')  # Use environment variable or default
conn = sqlite3.connect(db_path)

# Load CSV data (handle exceptions and allow for different file paths)
csv_file_path = os.environ.get('CSV_FILE_PATH', 'your_data.csv') # Use an environment variable or a default
try:
    df = pd.read_csv(csv_file_path)
    df.to_sql('sales', conn, if_exists='replace', index=False) # Consider 'append' if not replacing
    conn.commit() # Commit the changes after writing to the database
except FileNotFoundError:
    print(f"CSV file not found at path: {csv_file_path}. Check the CSV_FILE_PATH environment variable.")
    exit()
except Exception as e:
    print(f"An error occurred during data loading: {e}")
    exit()
finally:
    conn.close() # Ensure the connection is closed even if errors occur



# Dash app setup
app = dash.Dash(__name__)
server = app.server  # This line is crucial for deployment

# App layout
app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Country'].unique()],
        value=df['Country'].unique()[0] if len(df['Country'].unique()) > 0 else None, # Handle empty DataFrame
        multi=False,
        clearable=False
    ),
    dcc.Graph(id='sales-bar-chart'),
    dcc.Graph(id='customer-pie-chart')
])


# Callbacks for interactivity (connect to the database inside the callback for updated data)
@app.callback(
    [Output('sales-bar-chart', 'figure'), Output('customer-pie-chart', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_charts(selected_country):
    conn = sqlite3.connect(db_path) # Connect to the database within the callback
    filtered_df = pd.read_sql_query(f"SELECT * FROM sales WHERE Country = '{selected_country}'", conn)
    conn.close() # Close the connection after reading

    if filtered_df.empty:  # Handle cases where no data is returned
        return {}, {}

    bar_fig = px.bar(filtered_df, x='City', y='Customerid', title=f'Sales by City in {selected_country}')
    pie_fig = px.pie(filtered_df, names='Company', title=f'Customer Distribution by Company in {selected_country}')
    return bar_fig, pie_fig


if __name__ == '__main__':
    app.run_server(debug=True)