from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

app.config.from_mapping(
    SECRET_KEY='dev'  # Replace with a strong secret key in production
)


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
def dashboard():
    bar_data = query_db("SELECT product_category, SUM(sales) AS total_sales FROM sales GROUP BY product_category")
    bar_chart = go.Figure(data=[go.Bar(x=[row['product_category'] for row in bar_data],
                                        y=[row['total_sales'] for row in bar_data])])
    bar_chart.update_layout(title='Sales by Product Category')
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_data = query_db("SELECT product_category, SUM(sales) AS total_sales FROM sales GROUP BY product_category ORDER BY total_sales DESC LIMIT 5")
    pie_chart = go.Figure(data=[go.Pie(labels=[row['product_category'] for row in pie_data],
                                        values=[row['total_sales'] for row in pie_data])])
    pie_chart.update_layout(title='Top 5 Product Categories by Sales')
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)


if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True) # Ensure instance path exists
    app.run(debug=True)