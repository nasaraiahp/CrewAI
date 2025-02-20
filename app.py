# app.py (Flask application)
from flask import Flask, render_template
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Database setup (using a better approach for db creation)
DATABASE = 'sales_data.db'  # Centralized database name

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access data by column name
    return conn

def init_db():
    with app.app_context():  # Correct context for db operations with Flask
        conn = get_db_connection()
        cursor = conn.cursor()
        with open('schema.sql', mode='r') as f: # schema now in a separate file
            cursor.executescript(f.read())
        conn.commit()
        conn.close()

# Initialize the database only once
if not os.path.exists(DATABASE):
    init_db()


# Example schema.sql content for external schema management
# Note: schema.sql needs to be created manually next to the app.py file.
# ---
# CREATE TABLE IF NOT EXISTS sales (
#     product TEXT,
#     sales_amount REAL
# );
# INSERT OR IGNORE INTO sales (product, sales_amount) VALUES
# ('Product A', 1500),
# ('Product B', 1200),
# ('Product C', 2000),
# ('Product D', 800),
# ('Product E', 1700);
# ---



# Routes
@app.route('/')
def dashboard():
    conn = get_db_connection()
    sales_data = conn.execute("SELECT product, sales_amount FROM sales").fetchall()
    conn.close()


    bar_chart = create_bar_chart(sales_data)
    pie_chart = create_pie_chart(sales_data)

    return render_template('dashboard.html', bar_chart=bar_chart, pie_chart=pie_chart)


def create_bar_chart(sales_data):
    products = [row['product'] for row in sales_data]  # Accessing with column names
    amounts = [row['sales_amount'] for row in sales_data]
    fig = go.Figure(data=[go.Bar(x=products, y=amounts)])
    fig.update_layout(title="Sales by Product")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def create_pie_chart(sales_data):
    products = [row['product'] for row in sales_data]
    amounts = [row['sales_amount'] for row in sales_data]
    fig = go.Figure(data=[go.Pie(labels=products, values=amounts)])
    fig.update_layout(title="Sales Distribution")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == '__main__':
    app.run(debug=True) # Never have debug=True in production