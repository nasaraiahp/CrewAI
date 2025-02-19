from flask import Flask, render_template
import mysql.connector
import plotly.graph_objs as go
import plotly
import os

app = Flask(__name__)

# MySQL Database Configuration  (Better practice to store these securely, e.g., environment variables)
DB_HOST = os.environ.get("DB_HOST", "localhost")  # Default to localhost if not set
DB_USER = os.environ.get("DB_USER", "root")  # Get username; default if not available
DB_PASSWORD = os.environ.get("DB_PASSWORD")     # No default; MUST be set
DB_DATABASE = os.environ.get("DB_DATABASE", "sales_db") # Get DB name or default



@app.route("/")
def index():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        mycursor = mydb.cursor()

        # Fetch sales data (using parameterized queries or prepared statements is even better if dealing with user input)
        mycursor.execute("SELECT product, SUM(revenue) AS total_revenue FROM sales GROUP BY product")
        product_revenue = mycursor.fetchall()

        mycursor.execute("SELECT sale_date, SUM(revenue) AS daily_revenue FROM sales GROUP BY sale_date")
        daily_revenue = mycursor.fetchall()

        # ... (graph creation code - same as before)

    except mysql.connector.Error as err:
        print(f"Database error: {err}") # Log the error for debugging
        return "Database Error", 500 # Return an error page
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mycursor.close()
            mydb.close()

    return render_template('index.html', product_revenue_graph=product_revenue_graph, daily_revenue_graph=daily_revenue_graph)



if __name__ == "__main__":
    app.run(debug=False) # Disable debug mode in production