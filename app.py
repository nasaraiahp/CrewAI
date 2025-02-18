from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'sales_data.db')  # Store DB in the app's directory

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

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    sales_data = query_db('SELECT product, SUM(sales) as total_sales FROM sales GROUP BY product')

    if not sales_data: # Handle empty query result
        return render_template('error.html', message="No sales data found.")


    # Bar chart
    bar_chart = go.Figure(data=[go.Bar(
        x=[row['product'] for row in sales_data],
        y=[row['total_sales'] for row in sales_data],
        text=[f"Sales: {row['total_sales']}" for row in sales_data], # Tooltips for bar chart
        hoverinfo='text'
        )])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Pie chart (Donut Chart)
    labels = [row['product'] for row in sales_data]
    values = [row['total_sales'] for row in sales_data]
    pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3,
                                        hoverinfo='label+percent', textinfo='value')]) # Percentage and Value in Pie chart tooltips


    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

if __name__ == '__main__':
    app.run(debug=True) # Set to False in production