from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder
app.config['SECRET_KEY'] = os.urandom(24) # Add Secret Key for session security if needed later


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
    sales_data = query_db('SELECT product, sales FROM sales')

    # Plotly Bar Chart
    bar_chart = go.Figure(data=[go.Bar(x=[row['product'] for row in sales_data],
                                        y=[row['sales'] for row in sales_data])])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Plotly Pie Chart
    pie_chart = go.Figure(data=[go.Pie(labels=[row['product'] for row in sales_data],
                                        values=[row['sales'] for row in sales_data])])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_graph_json=bar_chart_json, pie_graph_json=pie_chart_json)


if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True) # Ensure instance path exists
    app.run(debug=False) # Disable debug mode in production