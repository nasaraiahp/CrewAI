import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import sqlite3
import pandas as pd
import os

# Database setup (using environment variables for security)
db_path = os.environ.get("SALES_DB_PATH", "sales_data.db")  # Use environment variable or default

# Create a connection function to manage connections effectively
def get_db_connection():
    return sqlite3.connect(db_path)

# Create sales data table (if it doesn't exist) within a function
def create_sales_table():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                product TEXT,
                category TEXT,
                sales_amount REAL
            )
        ''')

# Populate with dummy data (if table is empty) using parameterized query
def populate_dummy_data():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales")
        if cursor.fetchone()[0] == 0:  # Check if the table is empty
            dummy_data = [
                ('Product A', 'Category 1', 1200),
                ('Product B', 'Category 2', 800),
                ('Product C', 'Category 1', 1500),
                ('Product D', 'Category 2', 1000),
                ('Product E', 'Category 3', 600),
            ]
            conn.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
            conn.commit()


# Create the database and populate data on startup
create_sales_table()
populate_dummy_data()



# Create a Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children="Sales Dashboard"),

    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': 'All Categories', 'value': 'All Categories'}], # Initialize with 'All Categories'
        value='All Categories'
    ),

    dcc.Graph(id='sales-bar-chart'),
    dcc.Graph(id='sales-pie-chart')
])



# Callback to update charts and dropdown options dynamically
@app.callback(
    [Output('sales-bar-chart', 'figure'),
     Output('sales-pie-chart', 'figure'),
     Output('category-dropdown', 'options')],  # Update dropdown options
    [Input('category-dropdown', 'value')]
)
def update_charts(selected_category):
    with get_db_connection() as conn:  # Proper context management
        if selected_category == 'All Categories':
            df = pd.read_sql_query("SELECT * FROM sales", conn)
        else:
            # Parameterized query to prevent SQL injection
            df = pd.read_sql_query("SELECT * FROM sales WHERE category = ?", conn, params=(selected_category,))

        # Get distinct categories for dropdown
        categories = pd.read_sql_query("SELECT DISTINCT category FROM sales", conn)['category'].tolist()
        dropdown_options = [{'label': 'All Categories', 'value': 'All Categories'}] + [{'label': i, 'value': i} for i in categories]

    bar_fig = px.bar(df, x='product', y='sales_amount', title='Sales by Product')
    pie_fig = px.pie(df, values='sales_amount', names='product', title='Sales Distribution')
    return bar_fig, pie_fig, dropdown_options  # Return updated dropdown options


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)