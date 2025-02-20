import pandas as pd
import sqlite3
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Database setup
db_path = 'sales_data.db'  # Use a constant for the database path
conn = None  # Initialize connection object outside try block
try:
    # Use parameterized SQL to prevent SQL injection
    conn = sqlite3.connect(db_path)
    with conn:  # Use a context manager for automatic transaction management
        conn.execute('''
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
                SubscriptionDate DATE,
                Website TEXT
            )
        ''')

    # Load CSV data
    csv_file_path = 'your_data.csv'  # Use a variable for the file path
    if os.path.exists(csv_file_path):  # Check if the file exists before attempting to read
        try:
            df = pd.read_csv(csv_file_path)
            with conn:
                df.to_sql('customers', conn, if_exists='replace', index=False)
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV: {e}")
            # Handle parsing errors appropriately, e.g., log the error and exit or use a default dataframe
        except Exception as e:  # Catch other potential errors during data loading
            print(f"An error occurred during data loading: {e}")
    else:
        print(f"CSV file not found: {csv_file_path}")
        # Handle the case where the CSV file is not found. You might want to create a sample DataFrame or exit.

except sqlite3.Error as e:
    print(f"An error occurred during database operations: {e}")
finally:
    if conn:
        conn.close()  # Ensure the connection is closed in the finally block



# Dash app setup
app = dash.Dash(__name__)

# Data loading (outside the Dash app layout)
conn = sqlite3.connect(db_path)  # Reconnect to fetch data for the app
df = pd.read_sql_query("SELECT * FROM customers", conn) # Read data only after the table is created.
conn.close() # Close connection after data fetching


# Layout of the dashboard
app.layout = html.Div([
    html.H1("Sales Dashboard"),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Country'].unique()],
        value=df['Country'].iloc[0] if not df['Country'].empty else None,  # Handle empty DataFrame
        multi=False,
        clearable=False
    ),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='pie-chart'),
])


# Callbacks for interactivity
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_charts(selected_country):
    if selected_country is None: # Handle the case where there's no country selected (e.g., empty dataframe)
        return {}, {}, {} # Return empty figures
        
    filtered_df = df[df['Country'] == selected_country]

    bar_fig = px.bar(filtered_df, x='City', y='CustomerId', title=f'Customers by City ({selected_country})')

    # Convert SubscriptionDate to datetime outside the figure creation
    filtered_df['SubscriptionDate'] = pd.to_datetime(filtered_df['SubscriptionDate'], errors='coerce') # Handle invalid dates gracefully


    line_fig = px.line(filtered_df, x='SubscriptionDate', y='CustomerId', title=f'Customer Subscriptions Over Time ({selected_country})')

    pie_fig = px.pie(filtered_df, names='City', title=f'Customer Distribution by City ({selected_country})')

    return bar_fig, line_fig, pie_fig



if __name__ == '__main__':
    app.run_server(debug=True)