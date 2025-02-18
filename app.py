# app.py (Flask application)
import os
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Database setup and connection management
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access data by column name
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


# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)


def insert_dummy_data():
    with app.app_context():
        db = get_db()
        db.execute('DELETE FROM sales')  # Clear existing data
        dummy_data = [
            ('Product A', 120),
            ('Product B', 80),
            ('Product C', 150),
            ('Product D', 50),
            ('Product E', 100),
        ]
        db.executemany('INSERT INTO sales (product, sales_quantity) VALUES (?, ?)', dummy_data)
        db.commit()



@app.route('/')
def dashboard():
    with app.app_context():  # Correct context for database access
        db = get_db()
        sales_data = db.execute('SELECT * FROM sales').fetchall()

    # Create Plotly charts
    bar_chart = create_bar_chart(sales_data)
    pie_chart = create_pie_chart(sales_data)

    return render_template('dashboard.html', bar_chart=bar_chart, pie_chart=pie_chart)



def create_bar_chart(sales_data): #Moved outside app context as it does not use db
    products = [row['product'] for row in sales_data]
    quantities = [row['sales_quantity'] for row in sales_data]
    bar_chart = {
        "data": [go.Bar(x=products, y=quantities)],
        "layout": go.Layout(title="Sales by Product (Bar Chart)")
    }
    graphJSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_pie_chart(sales_data): #Moved outside app context as it does not use db
    products = [row['product'] for row in sales_data]
    quantities = [row['sales_quantity'] for row in sales_data]

    pie_chart = {
        "data": [go.Pie(labels=products, values=quantities)],
        "layout": go.Layout(title="Sales Distribution (Pie Chart)")
    }

    graphJSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON



if __name__ == '__main__':
    init_db()
    insert_dummy_data()
    app.run(debug=True)