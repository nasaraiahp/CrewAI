from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder
app.config['SECRET_KEY'] = os.urandom(24) # Add a secret key for session management (important if you later add features that use sessions)


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
    bar_chart_data = query_db("SELECT product_category, SUM(sales) AS total_sales FROM sales GROUP BY product_category")
    bar_labels = [row['product_category'] for row in bar_chart_data]
    bar_values = [row['total_sales'] for row in bar_chart_data]
    bar_chart = go.Figure(data=[go.Bar(x=bar_labels, y=bar_values)])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_chart_data = query_db("SELECT sales_region, SUM(sales) AS total_sales FROM sales GROUP BY sales_region")
    pie_labels = [row['sales_region'] for row in pie_chart_data]
    pie_values = [row['total_sales'] for row in pie_chart_data]
    pie_chart = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values)])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True) # Ensure instance folder exists
    app.run(debug=True)