import pandas as pd
import sqlite3
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from dash.dependencies import Input, Output
import os

# --- Database Operations ---
# Use environment variables for sensitive data like database paths
db_path = os.environ.get("DB_PATH", "customer_data.db")  # Default if env var not set
csv_file = os.environ.get("CSV_FILE_PATH", "customer_data.csv")

def create_and_populate_table(db_path, csv_file):
    try:
        conn = sqlite3.connect(db_path)  # No need for isolation_level in this context
        cursor = conn.cursor()

        # Parameterized query to prevent SQL injection (though not strictly needed for table creation)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                CustomerId INTEGER,
                FirstName TEXT,
                LastName TEXT,
                Company TEXT,
                City TEXT,
                Country TEXT,
                Phone1 TEXT,
                Phone2 TEXT,
                Email TEXT,
                SubscriptionDate TEXT,  # Store as TEXT to avoid potential date parsing errors
                Website TEXT
            )
        ''')

        # Efficiently load CSV using pandas' optimized to_sql
        df = pd.read_csv(csv_file)
        df.to_sql('customers', conn, if_exists='replace', index=False)
        conn.commit()
        print("Table created and populated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'conn' in locals():  # Ensure connection is closed even if an error occurs.
            conn.close()

# Create table outside the Dash app to avoid recreating on every refresh in debug mode
create_and_populate_table(db_path, csv_file)



# --- Dash App ---
app = dash.Dash(__name__)

# Separate layout definition for better readability
app.layout = html.Div([
    html.H1("Customer Data Dashboard"),
    dcc.Dropdown(
        id='chart-type',
        options=[
            {'label': 'Customers per Country', 'value': 'country'},
            {'label': 'Customers per City', 'value': 'city'},
            {'label': 'Subscription Date Distribution', 'value': 'subscription_date'},
            {'label': 'New Subscriptions Over Time', 'value': 'subscriptions_over_time'}
        ],
        value='country',
        clearable=False
    ),
    dcc.Graph(id='sales-chart')
])


@app.callback(
    Output('sales-chart', 'figure'),
    Input('chart-type', 'value')
)
def update_chart(chart_type):
    try:  # Add try-except for database connection in the callback
        conn = sqlite3.connect(db_path)
        # Use parameterized query even though chart_type is controlled by the dropdown
        df = pd.read_sql_query("SELECT * FROM customers", conn)  # Capitalize SQL keywords for clarity
        conn.close()


        fig = {}  # Initialize fig
        if chart_type == 'country':
            fig = px.histogram(df, x='Country', title="Number of Customers per Country")
        elif chart_type == 'city':
            fig = px.pie(df, names='City', title='Proportion of Customers by City')
        elif chart_type == 'subscription_date':
            df['SubscriptionDate'] = pd.to_datetime(df['SubscriptionDate'], errors='coerce')  # Handle parsing errors
            fig = px.histogram(df, x='SubscriptionDate', title='Distribution of Subscription Dates')
        elif chart_type == 'subscriptions_over_time':
            df['SubscriptionDate'] = pd.to_datetime(df['SubscriptionDate'], errors='coerce')
            subscriptions_over_time = df.groupby(pd.Grouper(key='SubscriptionDate', freq='M'))['CustomerId'].count().reset_index()
            fig = px.line(subscriptions_over_time, x='SubscriptionDate', y='CustomerId', title='New Subscriptions Over Time')

        return fig  # Return the figure after the if-elif block

    except Exception as e:  # Add error handling
        print(f"An error occurred in update_chart: {e}")
        return dash.no_update # or return an empty figure if no_update is causing issues.


if __name__ == '__main__':
    app.run_server(debug=True)  # Debug mode recommended for development, disable in production