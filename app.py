from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = 'sales_data.db'  # Define database path

# Database setup (using SQLite)
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

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Check if the database file exists and create it if it doesn't
if not os.path.exists(DATABASE):
    init_db()



@app.route('/')
def index():
    bar_data = query_db("SELECT product, sales_quantity FROM sales")
    bar_chart = go.Figure(data=[go.Bar(x=[row[0] for row in bar_data], y=[row[1] for row in bar_data])])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_data = query_db("SELECT category, SUM(sales_quantity) FROM sales GROUP BY category")
    pie_chart = go.Figure(data=[go.Pie(labels=[row[0] for row in pie_data], values=[row[1] for row in pie_data])])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart_json=bar_chart_json, pie_chart_json=pie_chart_json)

if __name__ == '__main__':
    app.run(debug=True) # Never enable debug mode in production