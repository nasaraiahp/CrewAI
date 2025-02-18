from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Configuration for secret key (important for security in production)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key' # Get from OS environment variable, or use default for development


def get_db():
    """Establishes a database connection if one doesn't exist, and reuses it if it does."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Return rows as dictionaries
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """Executes a database query."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    sales_data = query_db('SELECT * FROM sales')

    bar_chart = create_bar_chart(sales_data)
    pie_chart = create_pie_chart(sales_data)

    return render_template('index.html', bar_chart=bar_chart, pie_chart=pie_chart)


def create_bar_chart(sales_data):
    products = [row['product'] for row in sales_data]
    sales = [row['sales'] for row in sales_data]

    fig = go.Figure(data=[go.Bar(x=products, y=sales)])
    fig.update_layout(title='Sales by Product')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_pie_chart(sales_data):
    products = [row['product'] for row in sales_data]
    sales = [row['sales'] for row in sales_data]

    fig = go.Figure(data=[go.Pie(labels=products, values=sales)])
    fig.update_layout(title='Sales Distribution')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def init_db():
    """Initializes the database from the schema file."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Create the instance folder if it doesn't exist
os.makedirs(app.instance_path, exist_ok=True)

# Check if the database exists and create it if it doesn't
if not os.path.exists(DATABASE):
    init_db()

if __name__ == '__main__':
    app.run(debug=True)