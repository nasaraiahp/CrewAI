# app.py (Flask application)
import os
from flask import Flask, render_template
import mysql.connector
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Database credentials (securely store these)
DB_HOST = os.environ.get("DB_HOST", "localhost")  # Use environment variables
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "nasa") # NEVER store passwords directly in code. Use environment variables or a secrets management service.
DB_NAME = os.environ.get("DB_NAME", "sales_dashboard")


@app.route('/')
def index():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        mycursor = mydb.cursor()

        # Use parameterized queries to prevent SQL injection
        mycursor.execute("SELECT product, SUM(revenue) AS total_revenue FROM sales GROUP BY product")
        product_revenue = mycursor.fetchall()

        mycursor.execute("SELECT sales_date, SUM(revenue) AS daily_revenue FROM sales GROUP BY sales_date")
        daily_revenue = mycursor.fetchall()

    except mysql.connector.Error as err:
        # Handle database errors gracefully (log the error or display a user-friendly message)
        return f"Database error: {err}"  # In a real application, don't expose raw error details to the user.
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()



    # ... (chart creation code remains the same)

    return render_template('index.html', product_revenue_graphJSON=product_revenue_json, daily_revenue_graphJSON=daily_revenue_json)


if __name__ == '__main__':
    app.run(debug=True) # Disable debug mode in production!