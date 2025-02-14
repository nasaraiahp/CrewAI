# app.py
import sqlite3
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from flask_caching import Cache

# Configuration (consider moving to a separate config file or environment variables)
DATABASE_FILE = "sales_data.db"  # Avoid hardcoding paths
DEBUG_MODE = False  # Set to False for production

# Cache settings (improve performance for repeated queries)
CACHE_CONFIG = {
    "CACHE_TYPE": "filesystem",  # Consider Redis or Memcached for production
    "CACHE_DIR": "cache_directory"  # Specify a directory for caching
}

# Create the Dash app
app = dash.Dash(__name__)
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)


# Database connection function (using context manager for proper closing)
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None


# Initialize database and populate if empty
def initialize_database():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                region TEXT,
                product TEXT,
                sales INTEGER
            )
        ''')

        # Check if the table is empty before inserting sample data
        cursor.execute("SELECT COUNT(*) FROM sales")
        if cursor.fetchone()[0] == 0:
            sample_data = [
                ('North', 'Product A', 1200),
                ('North', 'Product B', 850),
                ('East', 'Product A', 1500),
                ('East', 'Product B', 1100),
                ('South', 'Product A', 900),
                ('South', 'Product B', 700),
                ('West', 'Product A', 1000),
                ('West', 'Product B', 950),
            ]
            cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", sample_data)
            conn.commit()
        conn.close()


# Call the database initialization function
initialize_database()

# Layout of the app
app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='product-dropdown',
        options=[],  # Options will be populated dynamically
        value=None  # Start with no initial value
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')
])

# Callback to populate the dropdown and update charts


@app.callback(
    [Output('product-dropdown', 'options'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('product-dropdown', 'value')]
)
@cache.memoize(timeout=60)  # Cache results for 60 seconds
def update_charts(selected_product):
    conn = get_db_connection()
    if not conn:
        return [], {}, {} # Return empty figures if no database connection

    # Query for available products
    products = pd.read_sql_query("SELECT DISTINCT product FROM sales", conn)
    dropdown_options = [{'label': p, 'value': p} for p in products['product']]

    if selected_product:
        df = pd.read_sql_query("SELECT * FROM sales WHERE product = ?", conn, params=(selected_product,))
    else:
        df = pd.DataFrame()  # Empty dataframe if no product selected


    conn.close()

    bar_fig = px.bar(df, x='region', y='sales', title=f'Sales by Region for {selected_product or "All Products"}')
    pie_fig = px.pie(df, values='sales', names='region', title=f'Sales Distribution for {selected_product or "All Products"}')

    return dropdown_options, bar_fig, pie_fig


if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE)