from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import json
import pandas as pd
import os

app = Flask(__name__)

# Database setup (use environment variables for sensitive data)
DATABASE = os.environ.get("DATABASE_URL", "sales_data.db")  # Default to local file if environment variable isn't set

# Use a connection pool for database connections
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # Access data by column name
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



def create_tables():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f: # Execute schema from file
            db.cursor().executescript(f.read())
        db.commit()


def populate_data(): # Dummy Data
    with app.app_context():
        db = get_db()
        sample_data = [
            ('Product A', 'Category 1', 1200),
            ('Product B', 'Category 2', 850),
            ('Product C', 'Category 1', 1550),
            ('Product D', 'Category 3', 900),
            ('Product E', 'Category 2', 1100),
            ('Product F', 'Category 1', 1700),
            ('Product G', 'Category 2', 780),
            ('Product H', 'Category 3', 1050),
        ]

        db.executemany("INSERT INTO sales (product, category, sales_amount) VALUES (?, ?, ?)", sample_data)
        db.commit()




@app.route('/')
def index():
    with app.app_context():
        df = pd.read_sql_query("SELECT * from sales", get_db())

        # Bar chart
        bar_chart = go.Figure(data=[go.Bar(x=df['product'], y=df['sales_amount'])])
        bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

        # Pie chart
        pie_chart = go.Figure(data=[go.Pie(labels=df['category'], values=df['sales_amount'])])
        pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)



if __name__ == '__main__':
    create_tables()  # Call this once to create tables initially
    #populate_data() # Run this only once to populate with sample data for testing
    app.run(debug=True)