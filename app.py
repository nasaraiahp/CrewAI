from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales.db')

# Database connection
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
        with app.open_resource('create_and_populate_db.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    db = get_db()
    sales_data = db.execute('SELECT product, SUM(sales) AS total_sales FROM sales GROUP BY product').fetchall()

    # Process data for Plotly charts
    product_sales = {}
    for row in sales_data:
        product_sales[row['product']] = row['total_sales']

    bar_chart = go.Figure(data=[go.Bar(x=list(product_sales.keys()), y=list(product_sales.values()))])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_chart = go.Figure(data=[go.Pie(labels=list(product_sales.keys()), values=list(product_sales.values()))])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True) # Ensure instance path exists
    init_db()  # Initialize the database on startup if it doesn't exist.
    app.run(debug=False) # Disable debug mode in production