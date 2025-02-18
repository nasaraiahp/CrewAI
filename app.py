import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# --- Data Management ---

# Use a persistent database file (or other appropriate data source)
db_path = "sales_data.db"  # Store data in a file
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the table exists before creating it
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales_data'")
table_exists = cursor.fetchone()

if not table_exists:  # Create the table only if it doesn't exist
    cursor.execute('''
        CREATE TABLE sales_data (
            product TEXT,
            category TEXT,
            sales REAL
        )
    ''')

    dummy_data = [
        ('Product A', 'Category 1', 1500),
        ('Product B', 'Category 2', 1200),
        ('Product C', 'Category 1', 2000),
        ('Product D', 'Category 3', 800),
        ('Product E', 'Category 2', 1800),
        ('Product F', 'Category 3', 950),
        ('Product G', 'Category 1', 1100),
        ('Product H', 'Category 2', 2300),
        ('Product I', 'Category 3', 1600)
    ]
    cursor.executemany('INSERT INTO sales_data VALUES (?,?,?)', dummy_data)
    conn.commit()

# Close the initial connection after setup. Reopen in callback for each query.
conn.close()



# --- Dash App ---

app = dash.Dash(__name__)
server = app.server  # Expose the Flask server


app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='chart-type',
        options=[{'label': i, 'value': i} for i in ['Bar Chart', 'Pie Chart']],
        value='Bar Chart',
        clearable=False
    ),
    dcc.Graph(id='sales-chart')
])


@app.callback(
    Output('sales-chart', 'figure'),
    Input('chart-type', 'value'))
def update_graph(chart_type):
    # Establish connection inside the callback function
    conn = sqlite3.connect(db_path)  # Connect each time data is needed.
    try:
        df = pd.read_sql_query("SELECT * from sales_data", conn)
        if chart_type == 'Bar Chart':
            fig = px.bar(df, x='product', y='sales', color='category',
                         title="Sales by Product and Category")
        elif chart_type == 'Pie Chart':
            fig = px.pie(df, values='sales', names='category',
                         title="Sales Distribution by Category")
        else:
            fig = {}  # Default empty figure

        return fig
    finally:
        conn.close()  # Close the connection in a finally block to ensure closure.



if __name__ == '__main__':
    app.run_server(debug=True)