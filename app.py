# app.py (Flask application)
import os
from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)
DATABASE = os.path.join(app.instance_path, 'sales_data.db')  # Store DB in instance folder

# Database setup (using application factory pattern for better testability and structure)
def create_app():
    app = Flask(__name__, instance_relative_config=True)  # instance_relative_config for better config management
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # Database connection using g object and a dedicated function
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            db.row_factory = sqlite3.Row # Use Row factory to access columns by name
        return db


    @app.teardown_appcontext # Closes the database at the end of each request
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @app.route('/')
    def index():
        db = get_db()
        sales_by_product = db.execute('SELECT product, SUM(sales) AS total_sales FROM sales GROUP BY product').fetchall()
        sales_by_region = db.execute('SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region').fetchall()

        # ... (chart creation code - unchanged from the original, except using db) ...

        return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)
        
    # Database initialization command (can be called with flask init-db)
    def init_db():
        with app.app_context():
            db = get_db()
            with app.open_resource('create_tables.sql', mode='r') as f:
                db.cursor().executescript(f.read())  # Improved DB initialization
            db.commit()
            with app.open_resource('populate_data.sql', mode='r') as f:
                db.cursor().executescript(f.read())  # Improved DB initialization
            db.commit() # Commit after inserts    

    app.cli.add_command(app.cli.command("init-db")(init_db)) # Registers the init-db command
    return app



app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # Never have debug=True in production