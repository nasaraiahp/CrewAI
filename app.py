# app.py
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'data.db')  # Store database in instance folder

# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Close database connection at the end of each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Execute SQL query
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Initialize database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Populate database (run only once initially)
def populate_db():
    sample_data = [
        ('Product A', 150),
        ('Product B', 200),
        ('Product C', 100),
        ('Product D', 250),
        ('Product E', 180),
    ]
    query_db("INSERT INTO sales (product, sales_quantity) VALUES (?, ?)", sample_data, one=False)



@app.route('/')
def index():
    sales_data = query_db("SELECT * FROM sales")

    # Create Bar Chart
    bar_chart = go.Figure(data=[go.Bar(x=[row['product'] for row in sales_data],
                                        y=[row['sales_quantity'] for row in sales_data])])
    bar_chart.update_layout(title_text='Product Sales')
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Create Pie Chart
    pie_chart = go.Figure(data=[go.Pie(labels=[row['product'] for row in sales_data],
                                        values=[row['sales_quantity'] for row in sales_data])])
    pie_chart.update_layout(title_text='Product Sales Distribution')
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           bar_chart=bar_chart_json, pie_chart=pie_chart_json)

if __name__ == "__main__":
    os.makedirs(app.instance_path, exist_ok=True) # Ensure instance path exists
    init_db()
    populate_db() # Uncomment for initial data population. Comment out afterwards.
    app.run(debug=True)