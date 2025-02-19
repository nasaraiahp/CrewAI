import os
from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)
DATABASE = 'sales_data.db'  # Define database path as a constant

# Database setup and connection management
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Check for database and initialize if not present
if not os.path.exists(DATABASE):
    init_db()


def populate_db():  # Separate population logic
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        dummy_data = [
            ('Product A', 'Electronics', 1500),
            ('Product B', 'Clothing', 1200),
            ('Product C', 'Electronics', 2000),
            ('Product D', 'Books', 800),
            ('Product E', 'Clothing', 900),
            ('Product F', 'Electronics', 1700),
            ('Product G', 'Books', 700),
            ('Product H', 'Clothing', 1000)
        ]

        try: # Check if data already exists to avoid duplication.
          cursor.execute("SELECT COUNT(*) from sales")
          if cursor.fetchone()[0] == 0: # populate only if the table is empty.
            cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
            db.commit()

        except sqlite3.OperationalError as e:
            # Handle the case where the table may not exist yet.
            if "no such table" in str(e):
                init_db()  # This will create the table if it doesn't exist.
                cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
                db.commit()
            else:
                print(f"An unexpected error occurred: {e}")

populate_db()

@app.route('/')
def index():
    db = get_db()
    df = pd.read_sql_query("SELECT * FROM sales", db)

    # Create charts
    bar_chart = go.Figure(data=[go.Bar(x=df['product'], y=df['sales_amount'])])
    bar_chart.update_layout(title='Sales by Product')

    pie_chart = go.Figure(data=[go.Pie(labels=df['category'], values=df['sales_amount'])])
    pie_chart.update_layout(title='Sales by Category')


    return render_template('index.html', bar_chart=bar_chart.to_json(), pie_chart=pie_chart.to_json())



if __name__ == '__main__':
    app.run(debug=True)