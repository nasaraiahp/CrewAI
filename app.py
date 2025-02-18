from flask import Flask, render_template, g
import sqlite3
import plotly.graph_objs as go
import pandas as pd
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales.db')  # Store DB in instance folder

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
        with app.open_resource('create_db.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route("/")
def index():
    db = get_db()
    try:
        sales_data = pd.read_sql_query("SELECT * FROM sales", db)
    except Exception as e:  # Basic error handling
        print(f"Database query error: {e}")  # Log the error.  Use a proper logger in production
        return "An error occurred while fetching data." # Return a user-friendly error message


    # Create charts (logic remains the same)
    bar_chart = go.Figure(data=[go.Bar(x=sales_data['product'], y=sales_data['sales'])])
    bar_chart.update_layout(title="Sales by Product")
    bar_chart_json = bar_chart.to_json()

    pie_chart = go.Figure(data=[go.Pie(labels=sales_data['region'], values=sales_data['sales'])])
    pie_chart.update_layout(title="Sales by Region")
    pie_chart_json = pie_chart.to_json()

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Initialize the database (remove this after first run if you don't want data reset on each run)
#init_db()  

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode in production!