# app.py (Flask application)
import os
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Ensure instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


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


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# Initialize database if it doesn't exist
if not os.path.exists(DATABASE):
    init_db()



# Populate database with dummy data (run once initially - now safer)
@app.route('/setup_db')
def setup_db():
    db = get_db()
    try:
        sample_data = [('Product A', 1500), ('Product B', 1200), ('Product C', 800), ('Product D', 2000), ('Product E', 1600)]
        db.executemany("INSERT INTO sales (product, sales) VALUES (?, ?)", sample_data)
        db.commit()
        return "Database setup complete!"
    except Exception as e:
        db.rollback() # Rollback on error to prevent partial updates.
        return f"Error setting up database: {e}"



@app.route('/')
def index():
    db = get_db()
    # Use parameterized queries to prevent SQL injection (though not strictly needed here, it's good practice).
    bar_data = db.execute("SELECT product, sales FROM sales").fetchall()
    pie_data = db.execute("SELECT product, sales FROM sales").fetchall()  # No need to fetch twice


    bar_chart = go.Figure(data=[go.Bar(x=[row['product'] for row in bar_data], y=[row['sales'] for row in bar_data])])
    bar_chart.update_layout(title="Product Sales")
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_chart = go.Figure(data=[go.Pie(labels=[row['product'] for row in pie_data], values=[row['sales'] for row in pie_data])])
    pie_chart.update_layout(title="Sales Distribution")
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_graphJSON=bar_chart_json, pie_graphJSON=pie_chart_json)


if __name__ == '__main__':
    app.run(debug=True)