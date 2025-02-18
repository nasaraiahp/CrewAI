from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'data.db')  # Define database path relative to the app

# Database connection using application context
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
    sales_data = query_db('SELECT product, SUM(sales) as total_sales FROM sales_data GROUP BY product')

    # Plotly Bar Chart
    bar_chart = {
        "data": [go.Bar(x=[row['product'] for row in sales_data],
                         y=[row['total_sales'] for row in sales_data])],
        "layout": go.Layout(title="Product Sales")

    }

    #Plotly Pie chart
    pie_labels = [row['product'] for row in sales_data]
    pie_values = [row['total_sales'] for row in sales_data]
    pie_chart = {
        "data": [go.Pie(labels=pie_labels, values=pie_values)],
        "layout": go.Layout(title="Sales Distribution")
    }

    bar_graph_JSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)
    pie_graph_JSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', bar_graph_JSON=bar_graph_JSON, pie_graph_JSON=pie_graph_JSON)


if __name__ == '__main__':
    app.run(debug=True) #Consider removing debug=True in production