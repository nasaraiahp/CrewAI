# app.py
import os
from flask import Flask, render_template
import sqlite3
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Database setup
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access data by column name
    return conn

def init_db():
    with app.app_context(): #Fixes RuntimeError: Working outside of application context.
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                product TEXT, 
                category TEXT, 
                sales_amount REAL
            )
        ''')
        dummy_data = [
            ('Product A', 'Electronics', 1500),
            ('Product B', 'Clothing', 800),
            ('Product C', 'Electronics', 1200),
            ('Product D', 'Books', 500),
            ('Product E', 'Clothing', 900),
            ('Product F', 'Electronics', 1000),
            ('Product G', 'Books', 600),
            ('Product H', 'Clothing', 700)
        ]
        cursor.executemany("INSERT OR IGNORE INTO sales VALUES (?, ?, ?)", dummy_data)
        conn.commit()


# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

init_db()


@app.route('/')
def index():
    conn = get_db_connection()
    sales_data = conn.execute("SELECT product, sales_amount FROM sales").fetchall()
    pie_data = conn.execute("SELECT category, SUM(sales_amount) FROM sales GROUP BY category").fetchall()    
    conn.close()  # Close connection after use

    bar_chart = create_bar_chart(sales_data)
    pie_chart = create_pie_chart(pie_data)

    return render_template('index.html', plot1=bar_chart, plot2=pie_chart)


def create_bar_chart(data):
    products = [row['product'] for row in data] # Use row factory to acces by name
    sales = [row['sales_amount'] for row in data]
    fig = go.Figure(data=[go.Bar(x=products, y=sales)])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_pie_chart(data):
    labels = [row['category'] for row in data]
    values = [row['SUM(sales_amount)'] for row in data] # Accessing by column name.
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON



if __name__ == '__main__':
    app.run(debug=True)