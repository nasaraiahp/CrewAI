# app.py (Improved)
from flask import Flask, render_template
import sqlite3
import plotly
import plotly.graph_objs as go

app = Flask(__name__)

# Database setup (replace with your actual database path)
DATABASE = 'sales_data.db'

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # Access data by column name
        return conn
    except sqlite3.Error as e:
        print(f"Database error: {e}") # Log the error for debugging
        return None # Or handle the error appropriately for your application


@app.route('/')
def index():
    conn = get_db_connection()
    if conn is None:
        return "Database error", 500 # Return an error response

    try:
        # Using parameterized query to prevent SQL injection (even though not strictly needed here, it demonstrates best practice)
        sales_data = conn.execute('SELECT * FROM sales').fetchall()

    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return "Error fetching data", 500
    finally:
        conn.close()  # Ensure connection is always closed

    # Data for Plotly charts
    product_categories = [row['product_category'] for row in sales_data]
    sales_figures = [row['sales'] for row in sales_data]
    profit_margins = [row['profit'] for row in sales_data]  # Added profit data

    # Create Bar Chart
    bar_chart = {
        "data": [go.Bar(x=product_categories, y=sales_figures)],
        "layout": go.Layout(title="Sales by Product Category")
    }

    # Create Pie Chart (using profit data)
    pie_chart = {
        "data": [go.Pie(labels=product_categories, values=profit_margins)],  # Profit pie chart
        "layout": go.Layout(title="Profit Distribution by Category")
    }



    return render_template('index.html', bar_chart=bar_chart, pie_chart=pie_chart)



if __name__ == '__main__':
    app.run(debug=True)