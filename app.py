from flask import Flask
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from pathlib import Path  # For database file handling

# Database Setup (Improved)
DATABASE_FILE = Path(__file__).parent / "sales_data.db"  # More robust file path handling

def create_database(db_file):
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            CREATE TABLE sales (
                date TEXT,
                product TEXT,
                category TEXT,
                region TEXT,
                sales REAL
            )
        ''')
        # Example data insertion (Adapt as needed)
        sample_data = [
            ('2024-01-01', 'Product A', 'Electronics', 'North', 1200),
            ('2024-01-01', 'Product B', 'Clothing', 'South', 850),
            ('2024-01-02', 'Product A', 'Electronics', 'East', 1500),
            # ... more sample data
            ('2024-01-15', 'Product C', 'Furniture', 'West', 1100)
        ]
        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?, ?)", sample_data)
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Table already exists
    finally:
        conn.close()


# Create the database if it doesn't exist
create_database(DATABASE_FILE)

# Flask and Dash Setup
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=['/assets/style.css'])  # External stylesheet loading


# Layout (with improved structure for responsiveness)
app.layout = html.Div([
    html.H1("Sales Dashboard"),

    html.Div([
        html.Div([  # Filter container
            html.Label("Date Range:"),
            dcc.DatePickerRange(
                id='date-range',
                start_date='2024-01-01',
                end_date='2024-01-15',
                min_date_allowed=df['date'].min(),  # Set date limits from data
                max_date_allowed=df['date'].max(),
                display_format='YYYY-MM-DD'  # Improve date display
            ),
            html.Label("Product:"),
            dcc.Dropdown(id='product-filter', multi=True),
            html.Label("Category:"),
            dcc.Dropdown(id='category-filter', multi=True),
            html.Label("Region:"),
            dcc.Dropdown(id='region-filter', multi=True)
        ], className='filter-container'),

        html.Div([  # Chart container with responsive layout using flexbox
            html.Div([dcc.Graph(id='sales-bar')], className="chart-item"),
            html.Div([dcc.Graph(id='sales-line')], className="chart-item")
        ], className="chart-container"),
        dcc.Graph(id='sales-pie', className="chart-item") # Included in the responsive layout
    ], className="dashboard-content"),

])


# Callbacks (with improved efficiency and data handling)
@app.callback(
    [Output('sales-bar', 'figure'),
     Output('sales-line', 'figure'),
     Output('sales-pie', 'figure'),
     Output('product-filter', 'options'),
     Output('category-filter', 'options'),
     Output('region-filter', 'options')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('product-filter', 'value'),
     Input('category-filter', 'value'),
     Input('region-filter', 'value')]
)
def update_charts(start_date, end_date, selected_products, selected_categories, selected_regions):
    # Database connection within the callback for better resource management
    conn = sqlite3.connect(DATABASE_FILE)
    try:
        df = pd.read_sql_query("SELECT * FROM sales", conn)
        df['date'] = pd.to_datetime(df['date'])
    finally:
        conn.close() #Ensure connection closes


    #Filtering (More efficient approach)
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    if selected_products:
        mask &= df['product'].isin(selected_products)
    if selected_categories:
        mask &= df['category'].isin(selected_categories)
    if selected_regions:
        mask &= df['region'].isin(selected_regions)
    filtered_df = df[mask]

    # ... (Rest of the chart creation code remains the same)

    return bar_chart, line_chart, pie_chart, product_options, category_options, region_options



# Define df here, accessible by app.layout and callbacks
conn = sqlite3.connect(DATABASE_FILE)
df = pd.read_sql_query("SELECT * FROM sales", conn) # dataframe available globally
df['date'] = pd.to_datetime(df['date']) # Convert date column outside callback
conn.close()

if __name__ == '__main__':
    app.run_server(debug=True)