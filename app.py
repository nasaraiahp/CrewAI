# app.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import os

# Database setup
db_file = 'sales_database.db'

# CSV file path (make it configurable)
csv_file_path = os.getenv('SALES_DATA_CSV', 'sales_data.csv') # Use environment variable or default

# Create the database file only if it doesn't exist.  This prevents overwriting.
if not os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
    try:
        df_csv = pd.read_csv(csv_file_path)  # Adjust data types if necessary
        df_csv.to_sql('sales', conn, if_exists='replace', index=False)
    except pd.errors.EmptyDataError:  # Handle empty CSV
        print("Error: sales_data.csv is empty or not found. Please provide valid data.")
        exit(1)  # Terminate if CSV is empty/missing
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
    finally:
        conn.close()


# Dash app initialization
app = dash.Dash(__name__)

# --- Prevent Cross-Site Scripting (XSS) ---
app.title = "Sales Dashboard"  # Set a title for the app

# --- Layout ---
app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='product-dropdown',
        options=[],  # Initialize as empty, will be populated in callback
        value=None,  # Don't set a default here, handle in callback after data load
        multi=False
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='pie-chart'),
])


# --- Callback to populate dropdown and update charts ---
@app.callback(
    [Output('product-dropdown', 'options'),
     Output('product-dropdown', 'value'),  # Set default value here
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')],
    Input('product-dropdown', 'value')
)
def update_dashboard(selected_product):
    conn = sqlite3.connect(db_file)
    try:
        df = pd.read_sql_query("SELECT * FROM sales", conn)

        # Populate dropdown options
        dropdown_options = [{'label': i, 'value': i} for i in df['Product'].unique()]
        default_value = df['Product'].iloc[0] if not df.empty else None

        # Filter data based on selected product
        if selected_product is not None:  # Handle initial callback where selected_product is None
            if isinstance(selected_product, str):
                filtered_df = df[df['Product'] == selected_product]
            elif isinstance(selected_product, list):  # For future multi-select support
                filtered_df = df[df['Product'].isin(selected_product)]
            else:
                filtered_df = df  # Default to show all if selected_product is invalid
        else:
            filtered_df = df


        # Create figures
        bar_fig = px.bar(filtered_df, x='Region', y='Sales', color='Product',
                         title=f'Sales by Region for {selected_product or "All Products"}')  # Handle None
        pie_fig = px.pie(filtered_df, values='Sales', names='Region',
                         title=f'Sales Distribution for {selected_product or "All Products"}')  # Handle None

        return dropdown_options, default_value, bar_fig, pie_fig

    except Exception as e:  # Handle errors
        print(f"An error occurred: {e}")
        return [], None, {}, {}  # Return empty values on error
    finally:
        conn.close()



if __name__ == '__main__':
    app.run_server(debug=True)