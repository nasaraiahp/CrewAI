from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Database setup
DATABASE = os.path.join(app.root_path, 'sales_data.db')  # Store DB in app directory

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row # Access data by name instead of index
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f: #Execute the SQL schema file
        db.cursor().executescript(f.read())
    db.commit()



@app.route('/')
def index():
    db = get_db()  #Using database connection

    # Data for bar chart (parameterized query)
    bar_data = db.execute("SELECT category, SUM(sales_quantity) AS total_sales FROM sales GROUP BY category").fetchall()
    bar_labels = [row['category'] for row in bar_data] #accessing by column name
    bar_values = [row['total_sales'] for row in bar_data]  #accessing by column name

    # Data for pie chart (parameterized query)
    pie_data = db.execute("SELECT product, sales_quantity FROM sales").fetchall()
    pie_labels = [row['product'] for row in pie_data]  #accessing by column name
    pie_values = [row['sales_quantity'] for row in pie_data]  #accessing by column name

    # ... (rest of the chart creation code is the same)


    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

#Register closing and initialize database functions
app.teardown_appcontext(close_db)
app.cli.command('initdb')(init_db)


if __name__ == '__main__':
    app.run(debug=True)