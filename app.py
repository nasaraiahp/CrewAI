from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

app.config.from_mapping(
    SECRET_KEY=os.urandom(16),  # Generate a random secret key
    DATABASE=DATABASE,
)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
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
        

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    db = get_db()
    sales_data = db.execute('SELECT * FROM sales').fetchall()
    
    # ... (chart creation code remains the same)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)



if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True)  # Ensure instance path exists
    app.run(debug=False) # Disable debug mode in production