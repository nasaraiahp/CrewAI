import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import sqlite3
import base64
import io
import os

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Database setup
db_name = "customer_data.db"

# Better practice to connect to the database only when needed
def get_db_connection():
    return sqlite3.connect(db_name, check_same_thread=False)


# Layout of the Dash app
app.layout = html.Div([
    html.H1("Customer Data Dashboard"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
    dash_table.DataTable(id='data-table', page_size=10),
])

# Callback to handle CSV upload and data processing
@app.callback([Output('output-data-upload', 'children'),
               Output('bar-chart', 'figure'),
               Output('pie-chart', 'figure'),
               Output('data-table', 'data'),
               Output('data-table', 'columns')],
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            # Database operations within a context manager
            with get_db_connection() as conn:
                cursor = conn.cursor()
                # Parameterized query to prevent SQL injection
                cursor.execute('''CREATE TABLE IF NOT EXISTS customers 
                               (Index1 INTEGER PRIMARY KEY AUTOINCREMENT, "Customer ID" TEXT, "First Name" TEXT, "Last Name" TEXT, 
                               Company TEXT, City TEXT, Country TEXT, "Phone 1" TEXT, "Phone 2" TEXT, Email TEXT, 
                               "Subscription Date" TEXT, Website TEXT)''')
                                # Let SQLite handle index automatically with AUTOINCREMENT                               
                df.to_sql('customers', conn, if_exists='replace', index=False)
                # commit happens automatically upon exiting 'with' block


            # Data Visualization
            bar_fig = px.bar(df, x='Country', y='Index1', title='Customer Distribution by Country')
            pie_fig = px.pie(df, values='Index1', names='Country', title='Customer Share by Country')

            table_columns = [{'name': i, 'id': i} for i in df.columns]
            table_data = df.to_dict('records')

            return html.Div([html.H5(f"Uploaded file: {filename}")]), bar_fig, pie_fig, table_data, table_columns
        except Exception as e:
            return html.Div([html.H5(f"There was an error processing this file. {e}")]), None, None, None, None # More informative error message

    return html.Div([html.H5("Please upload a CSV file.")]), None, None, None, None




if __name__ == '__main__':
    app.run_server(debug=True)