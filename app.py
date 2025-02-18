# app.py
import os
from flask import Flask, render_template
import sqlite3
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Database setup
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store database in instance folder

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(app.instance_path, exist_ok=True)  # Ensure instance path exists
    with app.app_context():
        conn = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        populate_database()



def populate_database():
    conn = get_db_connection()
    cur = conn.cursor()
    sample_data = [
        ('Product A', 15000),
        ('Product B', 25000),
        ('Product C', 10000),
        ('Product D', 30000),
        ('Product E', 20000)
    ]
    try:  # Use try-except to handle potential errors during insertion
        cur.executemany("INSERT INTO sales (product, sales_amount) VALUES (?, ?)", sample_data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Log the error for debugging
    finally:  # Ensure connection is closed in all cases
        conn.close()


@app.route('/')
def index():

    conn = get_db_connection()
    try:
        sales_data = conn.execute('SELECT * FROM sales').fetchall()
    except sqlite3.Error as e:  # Handle potential database errors
        print(f"Database error: {e}")
        sales_data = []  # Provide a default empty list in case of error
    finally:
        conn.close()

    bar_chart = go.Figure(data=[go.Bar(x=[row['product'] for row in sales_data],
                                        y=[row['sales_amount'] for row in sales_data])])

    pie_chart = go.Figure(data=[go.Pie(labels=[row['product'] for row in sales_data],
                                        values=[row['sales_amount'] for row in sales_data])])


    return render_template('index.html',
                           bar_chart=json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder),
                           pie_chart=json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder))


if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)