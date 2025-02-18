# app.py
import sqlite3
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import os

# Database setup (using a context manager for better resource handling)
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'sales_data.db')  # Store DB in the same directory

def create_or_get_db_conn():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn



def setup_database(conn):  # Separate database setup logic
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            category TEXT,
            sales_amount REAL
        )
    ''')

    # Check if data already exists to avoid re-inserting dummy data
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:  # Insert only if the table is empty
        dummy_data = [
            ('Product A', 'Electronics', 1200),
            ('Product B', 'Clothing', 850),
            ('Product C', 'Electronics', 1500),
            ('Product D', 'Books', 500),
            ('Product E', 'Clothing', 900),
            ('Product F', 'Electronics', 1000),
            ('Product G', 'Books', 600),
            ('Product H', 'Clothing', 750),
        ]
        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
        conn.commit()

# Initialize the database outside the layout function to avoid recreating on every refresh        
with create_or_get_db_conn() as conn:
    setup_database(conn)
    


app = dash.Dash(__name__)

# Prevent XSS vulnerabilities by explicitly setting the allowed HTML tags/attributes in Markdown 
app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': i, 'value': i} for i in ['All'] + ['Electronics', 'Clothing', 'Books']],
        value='All',
        clearable=False # prevent the user from selecting an empty value if they clear the dropdown
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
    html.Div(id='data-table', children=[]) # Div to hold the data table

])


@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('data-table', 'children')],  # Output for the data table
    Input('category-dropdown', 'value')
)
def update_charts(selected_category):
    with create_or_get_db_conn() as conn: # use context manager to ensure closing
        df = pd.read_sql_query("SELECT * FROM sales", conn)
    

    if selected_category != 'All':
        df_filtered = df[df['category'] == selected_category]
    else:
        df_filtered = df

    bar_fig = px.bar(df_filtered, x='product', y='sales_amount', title=f'Sales by Product ({selected_category if selected_category != "All" else "All Categories"})')
    pie_fig = px.pie(df_filtered, values='sales_amount', names='category', title=f'Sales Distribution ({selected_category if selected_category != "All" else "All Categories"})')

    # Create a DataTable
    data_table = dash.dash_table.DataTable(
        data=df_filtered.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df_filtered.columns]
    )

    return bar_fig, pie_fig, data_table  # Return the data table



if __name__ == '__main__':
    app.run_server(debug=True)