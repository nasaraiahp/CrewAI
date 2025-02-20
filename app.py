import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import sqlite3
import base64
import io
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Database setup (using a better file path)
db_path = os.path.join(os.getcwd(), 'customer_data.db')  # More robust path handling
# Or consider storing the database outside the application's directory for added security

def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            Index1 INTEGER,
            "Customer ID" INTEGER PRIMARY KEY,
            "First Name" TEXT,
            "Last Name" TEXT,
            Company TEXT,
            City TEXT,
            Country TEXT,
            "Phone 1" TEXT,
            "Phone 2" TEXT,
            Email TEXT,
            "Subscription Date" TEXT,
            Website TEXT
        )
    """)

# HTML layout
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
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


@app.callback(
    Output('output-data-upload', 'children'),
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except Exception as e:
            return html.Div([f'There was an error processing this file: {e}']), None, None  # More informative error message

        # Database operations (with better error handling and parameterized SQL)
        try:
            conn = sqlite3.connect(db_path)  # Use the defined db_path
            create_table(conn)  # Ensure table exists
            df.to_sql('customers', conn, if_exists='replace', index=False)
            conn.commit() # Important to commit changes
        except Exception as e:
            return html.Div([f'Database error: {e}']), None, None
        finally:
            if conn:
                conn.close()  # Always close the connection in a finally block

        # Create visualizations (using more descriptive axis labels)
        bar_fig = px.bar(df, x='Country', y='Customer ID', title='Customer Distribution by Country',
                         labels={'Customer ID': 'Number of Customers'})
        pie_fig = px.pie(df, values='Customer ID', names='City', title='Customer Distribution by City',
                         labels={'Customer ID': 'Number of Customers'})

        return html.Div(['Data uploaded and visualized successfully!']), bar_fig, pie_fig

    return html.Div(['Waiting for CSV upload...']), None, None



if __name__ == '__main__':
    app.run_server(debug=True)