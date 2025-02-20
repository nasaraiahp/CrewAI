# data_loader.py
import pandas as pd
import sqlite3
import os

def load_csv_to_sqlite(csv_file, db_file, table_name):
    """Loads data from a CSV file into an SQLite database table."""
    try:
        # Security improvement: Use parameterized SQL to prevent SQL injection
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create table if it doesn't exist (using parameterized SQL is not necessary here as table_name is not user-supplied)
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                Product TEXT,
                Sales REAL
            )
        ''')

        df = pd.read_csv(csv_file)  # Adjust data types as needed

        df.to_sql(table_name, conn, if_exists='replace', index=False)  # 'replace' or 'append'

        conn.commit()
        print(f"Data loaded successfully into table '{table_name}'.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()


# Example usage
DB_FILE = "sales_database.db"
if not os.path.exists(DB_FILE):  # Create the database only if it doesn't exist.
    load_csv_to_sqlite("sales_data.csv", DB_FILE, "sales")



# app.py (Dash app)
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

app = dash.Dash(__name__)
server = app.server  # Important for deployment

DB_FILE = "sales_database.db"  # Consistent database file name

# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),

    dcc.Graph(id='bar-chart'),

    dcc.Graph(id='pie-chart')

])


@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('bar-chart', 'relayoutData')  # Example: Update based on bar chart interaction
)
def update_charts(relayout_data):

    # Database connection is established within the callback for better resource management
    with sqlite3.connect(DB_FILE) as conn:
        # Query data from the database using Pandas
        query = "SELECT Product, Sales FROM sales"  # Replace 'sales' with your table name
        df = pd.read_sql_query(query, conn)

    # Create bar chart
    bar_fig = px.bar(df, x='Product', y='Sales', title='Sales by Product')

    # Create pie chart
    pie_fig = px.pie(df, values='Sales', names='Product', title='Sales Distribution')


    return bar_fig, pie_fig


if __name__ == '__main__':
    app.run_server(debug=True)