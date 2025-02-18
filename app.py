from flask import Flask, render_template, g  # Import g for database connection management
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales.db') # Store database in instance folder

# Ensure the instance folder exists
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


@app.route('/')
def index():
    db = get_db()
    sales_data = db.execute('SELECT * FROM sales').fetchall()
    # No need to manually close the connection here; teardown_appcontext handles it.

    bar_chart = create_bar_chart(sales_data)
    pie_chart = create_pie_chart(sales_data)

    return render_template('index.html', bar_graph_json=bar_chart, pie_graph_json=pie_chart)

# ... (rest of the code remains the same, except using db instead of conn)