# app.py
import sqlite3
import json
from flask import Flask, render_template
import plotly
import plotly.graph_objs as go
import os

app = Flask(__name__)

# Database setup (use environment variable for security)
DATABASE = os.environ.get("SALES_DATABASE", "sales_data.db")  # Default to sales_data.db if not set

def connect_db():
    return sqlite3.connect(DATABASE)


def get_db_cursor():  # Helper function to get a cursor within a context
    conn = connect_db()
    try:
        cursor = conn.cursor()
        yield cursor # Use yield to avoid manually closing in this function
    finally:
        conn.close()




def init_db(): # Function to initialize database, should only be called once
    with get_db_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    product TEXT,
                    category TEXT,
                    sales_amount REAL
                )
            ''')
            # Check if table is empty before inserting dummy data
            cursor.execute("SELECT COUNT(*) FROM sales")
            if cursor.fetchone()[0] == 0: # Only insert if table is empty
                dummy_data = [
                    ('Product A', 'Electronics', 1200),
                    ('Product B', 'Clothing', 850),
                    ('Product C', 'Books', 500),
                    ('Product D', 'Electronics', 1500),
                    ('Product E', 'Clothing', 600),
                    ('Product F', 'Books', 700)
                ]
                cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)


@app.route('/')
def index():
    with get_db_cursor() as cursor:
        try:
            cursor.execute("SELECT product, sales_amount FROM sales")
            sales_data = cursor.fetchall()

            cursor.execute("SELECT category, SUM(sales_amount) FROM sales GROUP BY category")
            category_data = cursor.fetchall()

            bar_chart = go.Figure(data=[go.Bar(x=[row[0] for row in sales_data], y=[row[1] for row in sales_data])])
            bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

            pie_chart = go.Figure(data=[go.Pie(labels=[row[0] for row in category_data], values=[row[1] for row in category_data])])
            pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

            return render_template('index.html', bar_graph_json=bar_chart_json, pie_graph_json=pie_chart_json)

        except Exception as e:
            print(f"Error fetching data: {e}")  # Log the error for debugging
            return "Error: Could not fetch data from the database", 500 # Return 500 error


if __name__ == '__main__':
    init_db() # Initialize the database on startup
    app.run(debug=True)  # Set debug=False for production