import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import sqlite3

# Database Configuration (Best practice: Store sensitive info outside the code)
DATABASE_FILE = 'sales_data.db'  # Or use environment variables


def create_connection(db_file):
    """ Creates a database connection. """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)  # Log the error for debugging
        return None


def create_table(conn):
    """ Creates the sales table if it doesn't exist. """
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                date DATE,
                product TEXT,
                region TEXT,
                sales INTEGER
            )
        ''')
        conn.commit()  # Commit the table creation
    except sqlite3.Error as e:
        print(e)  # Log the error

# Initialize the database connection outside the layout function
conn = create_connection(DATABASE_FILE)

if conn: # Check if the connection was successful
    create_table(conn)
    # Query all data initially inside the if statement to ensure conn exists
    df = pd.read_sql_query("SELECT * FROM sales", conn)

    # Close initial connection. Connections will be opened per callback for better concurrency handling
    conn.close()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Dashboard"),

    # Filters
    html.Div([
        html.Label("Date Range:"),
        dcc.DatePickerRange(
            id='date-range',
            display_format='YYYY-MM-DD',  # Format display
            persistence=True, persistence_type='local'  # Persist user selections
        ),
        html.Label("Product:"),
        dcc.Dropdown(
            id='product-dropdown',
            multi=True,
            persistence=True, persistence_type='local'
        ),
        html.Label("Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            multi=True,
            persistence=True, persistence_type='local'

        ),
    ]),

    # Charts
    html.Div([
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='line-chart'),
        dcc.Graph(id='pie-chart')
    ])
])



@app.callback(
    [Output('date-range', 'start_date'),
     Output('date-range', 'end_date'),
     Output('product-dropdown', 'options'),
     Output('product-dropdown', 'value'),
     Output('region-dropdown', 'options'),
     Output('region-dropdown', 'value'),
     Output('bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('product-dropdown', 'value'),
     Input('region-dropdown', 'value')],
    [State('product-dropdown', 'options'),
     State('region-dropdown', 'options')]
)
def update_charts(start_date, end_date, selected_products, selected_regions, product_options, region_options):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    conn = create_connection(DATABASE_FILE)
    if not conn:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, {}, {}, {}  # Return no_update if connection fails


    try:  # Wrap data fetching and filtering in try-except to handle errors safely
        df = pd.read_sql_query("SELECT * FROM sales", conn)


        if triggered_id is None:  # Initial load, set up dropdown options
            product_options = [{'label': i, 'value': i} for i in df['product'].unique()]
            selected_products = df['product'].unique()
            region_options = [{'label': i, 'value': i} for i in df['region'].unique()]
            selected_regions = df['region'].unique()
            start_date = df['date'].min()
            end_date = df['date'].max()

        # Convert date strings to datetime objects for comparison
        df['date'] = pd.to_datetime(df['date'])
        if start_date:
             start_date = pd.to_datetime(start_date)
        if end_date:
             end_date = pd.to_datetime(end_date)


        filtered_df = df[
            (df['date'] >= start_date) &
            (df['date'] <= end_date) &
            (df['product'].isin(selected_products or [])) &  # Handle empty selections
            (df['region'].isin(selected_regions or [])) ] # Handle empty selections



        bar_fig = px.bar(filtered_df, x='product', y='sales', color='region',
                         title="Sales by Product and Region")
        line_fig = px.line(filtered_df, x='date', y='sales', color='product',
                          title="Sales Trend over Time")
        pie_fig = px.pie(filtered_df, values='sales', names='region',
                        title="Sales Distribution by Region")


        return start_date, end_date, product_options, selected_products, region_options, selected_regions, bar_fig, line_fig, pie_fig

    except Exception as e:  # Catch and handle errors gracefully
        print(f"An error occurred: {e}")  # Log the error for debugging
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, {}, {}, {}  # Avoid crashing the app

    finally:
        if conn:  # Close the connection in the finally block to ensure closure
            conn.close()


if __name__ == '__main__':
    app.run_server(debug=True)