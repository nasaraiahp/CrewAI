# app.py (Flask application)
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

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

# Ensure the instance folder exists and create the DB if it doesn't
os.makedirs(app.instance_path, exist_ok=True)
if not os.path.exists(DATABASE):
    init_db()


# Example data loading (better to do this separately, not in the app code)
def load_sample_data():
    with app.app_context():
        db = get_db()
        db.execute("INSERT OR REPLACE INTO sales VALUES ('Product A', 15000)")
        db.execute("INSERT OR REPLACE INTO sales VALUES ('Product B', 22000)")
        db.execute("INSERT OR REPLACE INTO sales VALUES ('Product C', 18000)")
        db.execute("INSERT OR REPLACE INTO sales VALUES ('Product D', 25000)")
        db.commit()

# Uncomment to load sample data (usually you would load from csv, etc.)
# load_sample_data()



@app.route('/')
def index():
    db = get_db()
    sales_data = db.execute("SELECT * FROM sales").fetchall()

    # Create charts
    bar_chart = go.Figure(data=[go.Bar(x=[row[0] for row in sales_data], y=[row[1] for row in sales_data])])
    pie_chart = go.Figure(data=[go.Pie(labels=[row[0] for row in sales_data], values=[row[1] for row in sales_data])])

    # Use graph objects directly in the template or convert to JSON as needed
    return render_template('index.html', bar_chart=bar_chart, pie_chart=pie_chart)


if __name__ == '__main__':
    app.run(debug=True) #Never set debug to true in production, as it exposes a debugger interface to outside users.