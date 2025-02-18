# app.py (Flask application)
import sqlite3
import json
from flask import Flask, render_template, g
import plotly
import plotly.graph_objs as go

app = Flask(__name__)
DATABASE = 'sales_data.db'  # Store database name as a constant

# Database setup (using a function to get the database connection)
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

# Initialize the database if it doesn't exist. Check for table existence instead of row count.
try:
    with app.app_context():
        db = get_db()
        db.execute("SELECT * FROM sales LIMIT 1") # Check if the table exists
except sqlite3.OperationalError:
    init_db() # Initialize the database if the table does not exist


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def data():
    db = get_db()
    cursor = db.cursor()

    # Fetch sales data for bar chart
    cursor.execute("SELECT product, sales_quantity FROM sales")
    sales_data = cursor.fetchall()

    bar_chart = go.Figure(data=[go.Bar(x=[row[0] for row in sales_data], y=[row[1] for row in sales_data])])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Sales by category (for pie chart) – using parameterized query for potential future dynamic category input.  Not strictly necessary here, but demonstrates the principle.
    cursor.execute("SELECT category, SUM(sales_quantity) FROM sales GROUP BY category")
    category_sales = cursor.fetchall()
    pie_chart = go.Figure(data=[go.Pie(labels=[row[0] for row in category_sales],
                                     values=[row[1] for row in category_sales])])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


#  Move dummy data insertion to a separate function for clarity and to avoid accidental re-insertion.
def insert_dummy_data():
    with app.app_context():  # Ensure app context for database operations
        db = get_db()
        dummy_data = [
            ('Product A', 'Electronics', 120),
            ('Product B', 'Clothing', 85),
            ('Product C', 'Electronics', 200),
            ('Product D', 'Books', 50),
            ('Product E', 'Clothing', 150),
        ]
        try:
            db.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
            db.commit()
        except sqlite3.IntegrityError:  # Handle potential errors like duplicate entries if function is called repeatedly.
            pass

# Call this function to insert the data.
insert_dummy_data()

if __name__ == '__main__':
    app.run(debug=True)