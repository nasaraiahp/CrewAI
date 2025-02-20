# app.py
import pandas as pd
import sqlite3
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from flask import Flask, request
import os

# Security improvements: Use environment variables for sensitive data
DATABASE_URL = os.environ.get("DATABASE_URL", "customer_data.db")  # Default if not set

server = Flask(__name__)
app = Dash(__name__, server=server)

# Database connection (using SQLAlchemy for enhanced security)
from sqlalchemy import create_engine
engine = create_engine(f'sqlite:///{DATABASE_URL}') # Use SQLAlchemy for better DB interaction



def load_data(engine):
    try:
        df = pd.read_sql_table("customers", engine)
        return df
    except Exception as e:
        print(f"Error loading data from database: {e}")
        return None



def create_dashboard(df):
    if df is None:
        return html.Div([html.H1("Error: Could not load data.")]) # Display error message


    app.layout = html.Div([
        html.H1("Customer Data Dashboard"),

        dcc.Graph(id='customers-per-category', figure=create_customers_per_category(df)),
        dcc.Graph(id='customers-by-location', figure=create_customers_by_location(df)),
        dcc.Graph(id='subscription-dates-distribution', figure=create_subscription_dates_distribution(df)),
        dcc.Graph(id='new-subscriptions-trend', figure=create_new_subscriptions_trend(df)),
    ])

    return app

# ... (rest of the chart functions remain the same, but ensure data validation within those functions)


# Run the app (improved security and error handling)
if __name__ == '__main__':

    try:
        df = load_data(engine)  # Load data after app initialization
        if df is not None:

            app = create_dashboard(df)

            # Port Configuration (for external access if needed):
            # Use environment variable for PORT or default if not specified
            port = int(os.environ.get('PORT', 8050))
            app.run_server(debug=False, host='0.0.0.0', port=port)  # Important for deployment

        else:
            print("Failed to load data. Exiting.")

    except Exception as e:
        print(f"A critical error occurred: {e}")