# app.py
import sqlite3
from flask import Flask, render_template, jsonify, g

app = Flask(__name__)

# Database setup (use a more robust approach for production)
DATABASE = 'sales_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bar_chart_data')
def bar_chart_data():
    data = query_db('SELECT product, SUM(sales) AS total_sales FROM sales GROUP BY product')
    return jsonify({'labels': [row['product'] for row in data], 'values': [row['total_sales'] for row in data]})


@app.route('/pie_chart_data')
def pie_chart_data():
    data = query_db('SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region')
    return jsonify({'labels': [row['region'] for row in data], 'values': [row['total_sales'] for row in data]})

@app.route('/bar')
def bar_chart():
    return render_template('bar_chart.html')


@app.route('/pie')
def pie_chart():
    return render_template('pie_chart.html')


if __name__ == '__main__':
    # Database initialization (should be done in a separate script or migration)
    with app.app_context():  # Use app context for database operations in the initialization block.
        db = get_db()
        db.execute('CREATE TABLE IF NOT EXISTS sales (product TEXT, region TEXT, sales INTEGER)')

        # Check if data already exists to avoid duplicate entries on each run
        existing_data = query_db("SELECT * FROM sales")
        if not existing_data:  # Insert dummy data only if the table is empty.
            sales_data = [
                ('Product A', 'North', 1500),
                ('Product B', 'East', 1200),
                ('Product A', 'South', 1800),
                ('Product C', 'West', 2000),
                ('Product B', 'North', 1000),
            ]
            db.executemany('INSERT INTO sales (product, region, sales) VALUES (?, ?, ?)', sales_data)
            db.commit()



    app.run(debug=False) # Disable debug mode in production