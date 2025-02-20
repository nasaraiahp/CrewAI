# app.py
import sqlite3
import pandas as pd
import dash
from dash import html, dcc, Input, Output, State
import plotly.express as px
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.title = "Sales Dashboard"  # Set the title for the dashboard

# Database configuration using SQLAlchemy
app.server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales_data.db'  # Use SQLAlchemy for database management
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app.server)

# Define the database model
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CustomerId = db.Column(db.Integer)
    FirstName = db.Column(db.String(255))
    LastName = db.Column(db.String(255))
    Company = db.Column(db.String(255))
    City = db.Column(db.String(255))
    Country = db.Column(db.String(255))
    Phone1 = db.Column(db.String(255))
    Phone2 = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    SubscriptionDate = db.Column(db.String(255))  # Consider using a proper Date type if possible
    Website = db.Column(db.String(255))

    def __repr__(self):
        return f'<Sale {self.id}>'

# Create the database table if it doesn't exist. Remove the CSV loading part
# as the data should be directly added to the database if SQLAlchemy is used.
with app.server.app_context():
    db.create_all()

# Load CSV data only if the database table is empty. Data loading should be a separate process,
# not part of the application initialization.
with app.server.app_context():
    if not Sale.query.first():
        try:
            df = pd.read_csv('sales_data.csv')
            for _, row in df.iterrows():
                sale = Sale(**row.to_dict())
                db.session.add(sale)
            db.session.commit()
            print("Data loaded from CSV to database.")

        except FileNotFoundError:
             print("sales_data.csv not found. Starting with an empty database.")
        except Exception as e:
            print(f"Error loading data from CSV: {e}")
            db.session.rollback()


app.layout = html.Div([
    html.H1("Sales Dashboard"),
    dcc.Dropdown(
        id='chart-type',
        options=[{'label': i, 'value': i} for i in ['Bar Chart', 'Line Chart', 'Pie Chart']],
        value='Bar Chart'
    ),
    dcc.Graph(id='sales-chart'),
    dcc.Store(id='sales-data-store') # Store data in the browser to avoid repeated queries
])


@app.callback(
    Output('sales-chart', 'figure'),
    Output('sales-data-store', 'data'), # Store the data in the dcc.Store component
    Input('chart-type', 'value'),
    State('sales-data-store', 'data') # Get the stored data if available to reduce db calls
)
def update_chart(chart_type, stored_data):

    if stored_data is None: # if there is no stored data, fetch from db
        with app.server.app_context():
            df = pd.read_sql(Sale.query.statement, db.session.bind)
    else:
        df = pd.DataFrame(stored_data) # Get data from store. This can be useful for large datasets.


    if chart_type == 'Bar Chart':
        fig = px.bar(df, x='Country', y='CustomerId', title='Customers per Country')
    elif chart_type == 'Line Chart':
        fig = px.line(df, x='SubscriptionDate', y='CustomerId', title='Customer Subscriptions Over Time')
    elif chart_type == 'Pie Chart':
        fig = px.pie(df, values='CustomerId', names='Country', title='Customer Distribution by Country')
    else:
        fig = px.bar(df, x='Country', y='CustomerId', title='Customers per Country') # Default chart

    return fig, df.to_dict('records') # return the figure and updated store data


if __name__ == '__main__':
    app.run_server(debug=False, port=int(os.environ.get("PORT", 8050))) # Use environment variables for the port in production