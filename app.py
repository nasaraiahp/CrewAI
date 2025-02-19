from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import plotly.utils
import json
import os

app = Flask(__name__)
DATABASE = 'sales_data.db'  # Define database path as a constant

# Database setup and connection management
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access data by column name
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

def insert_sample_data():
    with app.app_context():
        db = get_db()
        sample_data = [
            ('Product A', 'Electronics', 120),
            ('Product B', 'Clothing', 85),
            ('Product C', 'Electronics', 200),
            ('Product D', 'Books', 50),
            ('Product E', 'Clothing', 150),
            ('Product F', 'Books', 70),
            ('Product G', 'Electronics', 100),
        ]
        db.executemany("INSERT OR IGNORE INTO sales VALUES (?, ?, ?)", sample_data)
        db.commit()


# Check if the database file exists and initialize if not
if not os.path.exists(DATABASE):
    init_db()
    insert_sample_data()



@app.route('/')
def dashboard():
    db = get_db()
    bar_data = db.execute("SELECT product, sales_quantity FROM sales").fetchall()
    pie_data = db.execute("SELECT category, SUM(sales_quantity) FROM sales GROUP BY category").fetchall()

    bar_chart = go.Figure(data=[go.Bar(x=[row['product'] for row in bar_data], y=[row['sales_quantity'] for row in bar_data])])
    bar_chart.update_layout(title='Product Sales')
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_chart = go.Figure(data=[go.Pie(labels=[row['category'] for row in pie_data], values=[row['SUM(sales_quantity)'] for row in pie_data])]) # Access using column names
    pie_chart.update_layout(title='Sales by Category')
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    app.run(debug=False) # Disable debug mode in production