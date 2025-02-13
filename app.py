import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import os

# Database setup (better practice to separate this)
DATABASE_PATH = os.path.join(os.getcwd(), 'sales_data.db')  # Use absolute path

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            product TEXT,
            category TEXT,
            sales_amount REAL
        )
    ''')
    # Use parameterized queries to prevent SQL injection (though not strictly needed for this static data)
    cursor.execute("INSERT OR IGNORE INTO sales (product, category, sales_amount) VALUES (?, ?, ?)", ('Product A', 'Electronics', 1500))
    cursor.execute("INSERT OR IGNORE INTO sales (product, category, sales_amount) VALUES (?, ?, ?)", ('Product B', 'Clothing', 1200))
    cursor.execute("INSERT OR IGNORE INTO sales (product, category, sales_amount) VALUES (?, ?, ?)", ('Product C', 'Electronics', 2000))
    cursor.execute("INSERT OR IGNORE INTO sales (product, category, sales_amount) VALUES (?, ?, ?)", ('Product D', 'Clothing', 800))
    conn.commit()
    conn.close()

# Create the database if it doesn't exist
if not os.path.exists(DATABASE_PATH):
    create_database(DATABASE_PATH)


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.title = "Sales Dashboard" # Set the title for the browser tab

server = app.server  # Expose the Flask server for deployment


app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in ['Electronics', 'Clothing']], # Prepend "All"
        value='All'
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart')
])

@app.callback(
    [Output('bar-chart', 'figure'), Output('pie-chart', 'figure')],
    [Input('category-dropdown', 'value')]
)
def update_charts(selected_category):
    conn = sqlite3.connect(DATABASE_PATH)  # Use the defined path
    try:
        df = pd.read_sql_query("SELECT * FROM sales", conn)
    except Exception as e:  # Handle potential database errors
        print(f"Database Error: {e}")
        return dash.no_update, dash.no_update  # Return no_update in case of error
    finally:
        conn.close()


    if selected_category != 'All':
        df = df[df['category'] == selected_category]

    bar_fig = px.bar(df, x='product', y='sales_amount', title='Sales by Product')
    pie_fig = px.pie(df, values='sales_amount', names='product', title='Sales Distribution')

    return bar_fig, pie_fig



if __name__ == '__main__':
    app.run_server(debug=True)