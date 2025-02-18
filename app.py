import os
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'sales_data.db')  # Store DB in app's directory

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access data by column names
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
    sales_by_product = query_db('SELECT product, SUM(sales) AS total_sales FROM sales GROUP BY product')
    sales_by_region = query_db('SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region')

    # ... (chart creation code remains the same) ...

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

def init_db():
    with app.app_context():  # Correct context for db operations within the app
        db = get_db()
        with app.open_resource('create_and_populate_db.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    if not os.path.exists(DATABASE):  # Check and initialize db only if it doesn't exist
        init_db()
    app.run(debug=True) # Consider setting to False in a production setting.