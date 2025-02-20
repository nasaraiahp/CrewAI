# app.py
import os
from flask import Flask, render_template
import sqlite3
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)

# Database setup (better practice for Flask apps)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')

def get_db():
    db = getattr(g, '_database', None)  # Use g to avoid multiple db connections per request
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row #for better row access
    return db

def close_connection(exception): # close db connection after request
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    
@app.teardown_appcontext
def teardown_db(exception): # Ensure db is closed at the end of request
    close_connection(exception)



def init_db(): # Initialize database
    with app.app_context(): #Ensures we have app's context
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        populate_db(db)


def populate_db(db):  # Populate with dummy data if table is empty
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:  # Check if table is empty
        dummy_data = [
            ('Product A', 'Electronics', 150),
            ('Product B', 'Clothing', 200),
            ('Product C', 'Electronics', 100),
            ('Product D', 'Books', 120),
            ('Product E', 'Clothing', 80),
            ('Product F', 'Books', 180)
        ]
        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", dummy_data)
        db.commit()



@app.route('/')
def dashboard():
    db = get_db() # Get DB
    populate_db(db) # Populate database if empty
    df = pd.read_sql_query("SELECT * from sales", db)


    # ... (chart creation code remains the same)

    return render_template('dashboard.html', 
                           bar_chart_json=bar_chart.to_json(), 
                           pie_chart_json=pie_chart.to_json())



if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True) # Makes the instance folder if needed
    init_db() # Initialise DB only once
    app.run(debug=True)