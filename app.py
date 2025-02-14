from flask import Flask, render_template, request, g
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder
app.config['SECRET_KEY'] = os.urandom(24) # Important for session security in Flask


def get_db():
    """Establishes a database connection if one doesn't exist."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access data by column name
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection after each request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    """Initializes the database using the schema.sql file."""
    with app.app_context():  # Ensures application context for database operations
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# For local development, create the instance folder if it doesn't exist
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

# Initialize the database on startup (ensure this is not run in production if the db already exists and has data)
init_db()


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bar_chart")
def bar_chart():
    db = get_db()
    data = db.execute("SELECT product, sales_amount FROM sales").fetchall()
    products = [row['product'] for row in data]  # Access data by column name
    sales = [row['sales_amount'] for row in data]

    # ... (rest of the chart generation code remains the same)


@app.route("/pie_chart")
def pie_chart():
    db = get_db()
    data = db.execute("SELECT product, sales_amount FROM sales").fetchall()
    products = [row['product'] for row in data]
    sales = [row['sales_amount'] for row in data]

    # ... (rest of the chart generation code remains the same)



if __name__ == "__main__":
    app.run(debug=True)