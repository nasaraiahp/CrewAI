# app.py
import os
from flask import Flask, render_template, request
import sqlite3
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)

DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(app.instance_path, exist_ok=True)  # Ensure instance path exists
    with app.app_context():  # access the app context inside this function
        conn = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    conn = get_db_connection()
    df_bar = df_pie = pd.DataFrame()  # Initialize even if query fails
    error = None
    chart_types = {'bar': 'Sales by Product Category', 'pie': 'Sales Distribution by Region'}


    if request.method == 'POST':
        selected_chart_type = request.form.get('chart_type')
        if selected_chart_type not in chart_types:  # Validate input
            error = "Invalid chart type selected"

    selected_chart_type = request.form.get('chart_type', 'bar')  # Default to 'bar'


    try:
        if selected_chart_type == 'bar':
            df_bar = pd.read_sql_query("SELECT product_category, SUM(sales) AS total_sales FROM sales GROUP BY product_category", conn)

        elif selected_chart_type == 'pie':
            df_pie = pd.read_sql_query("SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region", conn)


    except sqlite3.Error as e:  # Catch db errors
        error = f"Database error: {e}"
    finally: # Always close after use
        conn.close()

    # Create charts only if data is available
    bar_chart_json = pie_chart_json = None

    if not df_bar.empty:
        bar_chart = go.Figure(data=[go.Bar(x=df_bar['product_category'], y=df_bar['total_sales'])])
        bar_chart.update_layout(title=chart_types.get('bar', 'Bar Chart')) # Use dict to lookup
        bar_chart_json = bar_chart.to_json()
    
    if not df_pie.empty:
        pie_chart = go.Figure(data=[go.Pie(labels=df_pie['region'], values=df_pie['total_sales'])])
        pie_chart.update_layout(title=chart_types.get('pie', 'Pie Chart'))
        pie_chart_json = pie_chart.to_json()


    return render_template('dashboard.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json, chart_types=chart_types, selected_chart_type=selected_chart_type, error=error)



if __name__ == '__main__':
    init_db() # Initialize the database
    app.run(debug=True)