from flask import Flask, render_template, g  # Import g for database connection management
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Configuration (consider moving to a separate config file for better management)
DATABASE = os.path.join(app.root_path, 'sales_data.db') # Construct absolute database path
app.config['SECRET_KEY'] = os.urandom(24) # Generate a strong secret key for session management (if needed)



# Database connection (improved using g object for better connection handling)
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE) # Use app.config['DATABASE'] if using a config file
        g.db.row_factory = sqlite3.Row  # Access data by column names
    return g.db

def close_db(e=None): # Handle closing the database connection after requests
    db = g.pop('db', None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_db) # Register the close_db function to be called after each request


@app.route('/')
def index():
    db = get_db()

    # Query data for charts
    # Use parameterized queries or ORM to prevent SQL injection vulnerabilities
    try:
        bar_query = "SELECT product_category, SUM(sales) AS total_sales FROM sales GROUP BY product_category"
        bar_data = db.execute(bar_query).fetchall()

        pie_query = "SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region"
        pie_data = db.execute(pie_query).fetchall()
    except Exception as e:  # Handle potential database errors
        # Log the error appropriately (e.g., to a file or console) in a production environment
        return render_template("error.html", error=str(e)), 500  # Use custom error template


    # Data processing (can be optimized if data volume is large)
    bar_labels = [row['product_category'] for row in bar_data]
    bar_values = [row['total_sales'] for row in bar_data]

    pie_labels = [row['region'] for row in pie_data]
    pie_values = [row['total_sales'] for row in pie_data]


    # Chart creation
    bar_chart = go.Figure(data=[go.Bar(x=bar_labels, y=bar_values)])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_chart = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values)])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)



    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)




if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode in production