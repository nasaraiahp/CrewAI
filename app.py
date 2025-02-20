# app.py
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import sqlite3
import base64
import io
import os

app = dash.Dash(__name__)

# Database setup (better to do this outside the callback)
db_path = "customer_data.db"  # Use a consistent path
if not os.path.exists(db_path):  # Create the database if it doesn't exist
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE customers (
            "Index" INTEGER PRIMARY KEY AUTOINCREMENT,  -- Make Index a primary key
            "Customer ID" INTEGER,
            "First Name" TEXT,
            "Last Name" TEXT,
            "Company" TEXT,
            "City" TEXT,
            "Country" TEXT,
            "Phone 1" TEXT,
            "Phone 2" TEXT,
            "Email" TEXT,
            "Subscription Date" TEXT,
            "Website" TEXT
        )
    ''')  # Use parameterized queries or a safer method to create the table schema
    conn.commit()
    conn.close()


# HTML layout
app.layout = html.Div([
    html.H1("Customer Data Dashboard"),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV'),
        multiple=False,
        accept=".csv"  # Restrict to CSV files
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')
])


# Callback to handle data upload and display
@app.callback(
    Output('output-data-upload', 'children'),
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        try:  # Add try-except block for better error handling
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            # Store data in SQLite database (using context manager)
            conn = sqlite3.connect(db_path)
            df.to_sql('customers', conn, if_exists='replace', index=False) # Consider 'append' instead of 'replace'
            conn.close()

            # Create bar chart
            bar_fig = px.bar(df, x='Country', y='Customer ID', title='Customers per Country')

            # Create pie chart
            city_counts = df['City'].value_counts()
            pie_fig = px.pie(city_counts, values=city_counts.values, names=city_counts.index,
                             title='Customer Distribution by City')

            # Display the uploaded data as a table
            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                page_size=10  # Add pagination for large datasets
            )

            return table, bar_fig, pie_fig
        except Exception as e:
            return html.Div(f"Error processing file: {e}"), None, None # Display error messages

    return None, None, None  # Return None for figures if no data is uploaded



if __name__ == '__main__':
    app.run_server(debug=True)