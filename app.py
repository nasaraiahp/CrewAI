from flask import Flask, render_template
import mysql.connector
import plotly
import plotly.graph_objs as go
import json
import os

app = Flask(__name__)

# Get database credentials from environment variables (BEST PRACTICE)
DB_HOST = os.environ.get("DB_HOST", "localhost")  # Default to localhost if not set
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD")  # No default password
DB_NAME = os.environ.get("DB_NAME", "sales_db")


@app.route("/")
def index():
    try:
        # Create connection inside the function (better for handling potential errors)
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM sales_data")
        sales_data = mycursor.fetchall()

        products = [row[0] for row in sales_data]
        sales = [row[1] for row in sales_data]

        # ... (chart creation code remains the same)

    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")  # Log the error
        return "Database error", 500  # Return an error response to the user
    finally:
        if 'mydb' in locals() and mydb.is_connected():  # Always close the connection
            mycursor.close()
            mydb.close()

    return render_template('index.html', bar_chart=bar_chart_json, pie_chart=pie_chart_json)

if __name__ == "__main__":
    app.run(debug=False) # Disable debug mode in production