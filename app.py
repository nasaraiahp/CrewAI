# app.py
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import sqlite3
from flask import Flask
import os
import base64
import io

server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True) # Suppress callback exceptions for better error handling

# Database setup (consider environment variables for sensitive data)
DATABASE_URL = os.environ.get("DATABASE_URL", "customer_data.db")  # Use environment variable if available, fallback to local file

def create_table():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            Index INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID TEXT UNIQUE,  -- Add UNIQUE constraint to CustomerID
            FirstName TEXT,
            LastName TEXT,
            Company TEXT,
            City TEXT,
            Country TEXT,
            Phone1 TEXT,
            Phone2 TEXT,
            Email TEXT,
            SubscriptionDate TEXT,
            Website TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()


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
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')
])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            # Data validation - Example: Check for required columns
            required_columns = ['CustomerID', 'FirstName', 'LastName', 'Country'] # Example
            if not all(col in df.columns for col in required_columns):
                return html.Div(['Error: Missing required columns.'])


            conn = sqlite3.connect(DATABASE_URL)
            df.to_sql('customers', conn, if_exists='replace', index=False) # Consider 'append' if not replacing
            conn.close()

            return html.Div([
                html.H5(f'Successfully uploaded {filename}') # More descriptive message
            ])

        except Exception as e:
            print(e) # Log the error for debugging
            return html.Div([html.H5(f'There was an error processing this file: {e}')]) # Show error to user


@app.callback(
    [Output('bar-chart', 'figure'), Output('pie-chart', 'figure')],
    Input('output-data-upload', 'children')  # Triggered after upload
)
def update_graphs(_):  # The input isn't directly used but the callback needs a trigger
    conn = sqlite3.connect(DATABASE_URL)
    df = pd.read_sql_query("SELECT * from customers", conn)  # Parameterize query if taking user input later
    conn.close()

    bar_fig = px.bar(df, x='Country', y='Index', title='Customer Distribution by Country')
    pie_fig = px.pie(df, names='Country', title='Customer Proportion by Country')

    return bar_fig, pie_fig




if __name__ == '__main__':
    app.run_server(debug=True)