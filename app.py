from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Configuration for secret key (IMPORTANT: Do this securely in a production environment!)
app.config['SECRET_KEY'] = 'your_secret_key' # Replace with a strong, randomly generated key

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


@app.teardown_appcontext
def close_db(error=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()



def init_db():
    db = get_db()
    with app.open_resource('create_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.route('/')
def index():
    db = get_db()
    sales_data = db.execute('SELECT product, sales, category FROM sales').fetchall()  # Select only needed columns

    # Create Bar Chart
    bar_chart = go.Figure(data=[go.Bar(x=[row['product'] for row in sales_data],
                                        y=[row['sales'] for row in sales_data])])
    bar_chart_JSON = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Create Pie Chart
    categories = {}
    for row in sales_data:
        category = row['category']
        categories[category] = categories.get(category, 0) + row['sales'] # Use get() for simpler aggregation

    pie_chart = go.Figure(data=[go.Pie(labels=list(categories.keys()), values=list(categories.values()))])
    pie_chart_JSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', bar_chart=bar_chart_JSON, pie_chart=pie_chart_JSON)


# Create the instance folder if it doesn't exist
os.makedirs(app.instance_path, exist_ok=True)

# Initialize the database
init_db()


if __name__ == '__main__':
    app.run(debug=True) # Remember to set debug=False for production