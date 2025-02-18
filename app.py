# app.py
import os
from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Database setup and management
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

def populate_db():  # Separate data population
    with app.app_context():
        db = get_db()
        dummy_data = [
            ('Product A', 'Electronics', 1500),
            ('Product B', 'Clothing', 1200),
            # ... (rest of the dummy data)
        ]
        db.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
        db.commit()


# Initialize database if it doesn't exist
if not os.path.exists(DATABASE):
    os.makedirs(app.instance_path, exist_ok=True) # Ensure instance path exists
    init_db()
    populate_db()



# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bar_chart')
def bar_chart():
    df = pd.read_sql_query("SELECT * FROM sales", get_db())
    fig = go.Figure(data=[go.Bar(x=df['product'], y=df['sales_amount'])])
    graphJSON = fig.to_json()
    return render_template('bar_chart.html', graphJSON=graphJSON)


@app.route('/pie_chart')
def pie_chart():
    df = pd.read_sql_query("SELECT category, SUM(sales_amount) AS total_sales FROM sales GROUP BY category", get_db())
    fig = go.Figure(data=[go.Pie(labels=df['category'], values=df['total_sales'])])
    graphJSON = fig.to_json()
    return render_template('pie_chart.html', graphJSON=graphJSON)




if __name__ == '__main__':
    app.run(debug=True)