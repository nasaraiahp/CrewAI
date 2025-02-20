# data_loader.py
import pandas as pd
import sqlite3
import os

def load_csv_to_sqlite(csv_file, db_file, table_name):
    """Loads data from a CSV file into an SQLite database table."""

    try:
        # Use pathlib for better path handling
        db_path = os.path.abspath(db_file)

        conn = sqlite3.connect(db_path)  # Apply absolute path for database file
        cursor = conn.cursor()

        # Parameterize the query to prevent SQL injection (though low risk here, it's good practice)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        if not cursor.fetchone():
            # Create the table if it doesn't exist
            df = pd.read_csv(csv_file)  # Read CSV to infer schema
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Table '{table_name}' created and data loaded successfully.")
        else:
            df = pd.read_csv(csv_file)
            df.to_sql(table_name, conn, if_exists='append', index=False)  # Append if table exists
            print(f"Data loaded into existing table '{table_name}' successfully.")

        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()


# app.py (Dash app)
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import os


app = dash.Dash(__name__)

DATABASE_PATH = os.path.abspath('sales_data.db')

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Sales Data Dashboard"),

    # Dropdown for Country selection
    dcc.Dropdown(id='country-dropdown',
                 options=[],  # Dynamically populated later
                 value=None,  # Ensure initial value is None for multi-select
                 multi=True,
                 placeholder="Select Country/Countries"
                 ),

    dcc.Graph(id='sales-bar-chart'),
    dcc.Graph(id='customer-pie-chart')
])


@app.callback(
    [Output('sales-bar-chart', 'figure'),
     Output('customer-pie-chart', 'figure'),
     Output('country-dropdown', 'options')],
    Input('country-dropdown', 'value')

)
def update_charts(selected_countries):
    conn = sqlite3.connect(DATABASE_PATH) 
    
    # Use parameterized queries consistently to prevent SQL injection
    base_pie_query = "SELECT Country, COUNT(*) AS CustomerCount FROM customers GROUP BY Country"
    base_bar_query = "SELECT SubscriptionDate, COUNT(*) AS SubscriptionCount FROM customers GROUP BY SubscriptionDate"


    if selected_countries:
        pie_query = f"SELECT Country, COUNT(*) AS CustomerCount FROM customers WHERE Country IN ({','.join('?'*len(selected_countries))}) GROUP BY Country"
        bar_query = f"SELECT SubscriptionDate, COUNT(*) AS SubscriptionCount FROM customers WHERE Country IN ({','.join('?'*len(selected_countries))}) GROUP BY SubscriptionDate"

        df_pie = pd.read_sql_query(pie_query, conn, params=selected_countries)
        df_bar = pd.read_sql_query(bar_query, conn, params=selected_countries)

    else:
        df_pie = pd.read_sql_query(base_pie_query, conn)  # Execute query without WHERE clause if no countries selected
        df_bar = pd.read_sql_query(base_bar_query, conn)



    pie_chart = px.pie(df_pie, values='CustomerCount', names='Country', title='Customer Distribution by Country')
    bar_chart = px.bar(df_bar, x='SubscriptionDate', y='SubscriptionCount', title='Subscriptions Over Time')

    # Populate dropdown options
    country_options = [{'label': country, 'value': country} for country in pd.read_sql_query("SELECT DISTINCT Country FROM customers", conn)['Country'].unique()]
    conn.close()

    return bar_chart, pie_chart, country_options



if __name__ == '__main__':
    # Load data if the database doesn't exist yet
    if not os.path.exists("sales_data.db"):
        load_csv_to_sqlite("customer_data.csv", "sales_data.db", "customers")  # Make sure customer_data.csv exists


    app.run_server(debug=True)