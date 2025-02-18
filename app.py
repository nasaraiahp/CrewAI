from flask import Flask, render_template, g
import sqlite3
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'sales_data.db')  # Store DB path securely

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Access data by column name
    return g.db

@app.teardown_appcontext  # Ensure proper connection closing after request
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    db = get_db()
    sales_data = db.execute('SELECT * FROM sales').fetchall()

    # ... (chart creation code remains the same)

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

if __name__ == '__main__':
    app.run(debug=False) # Disable debug mode in production