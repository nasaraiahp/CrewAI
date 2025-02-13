import os
from flask import Flask, render_template, jsonify
import mysql.connector
import plotly.graph_objs as go
import plotly
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Database credentials from environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DATABASE = os.environ.get("DB_DATABASE")

def get_db_connection():
    """Establishes a database connection and returns a cursor object."""
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


def create_sales_table(cursor):
    """Creates the sales table if it doesn't exist."""
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                Price DECIMAL(10, 2),
                LocationName VARCHAR(255),
                ProductName VARCHAR(255),
                ProductID INT
            )
        """)
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def insert_sample_data(cursor, connection):
    """Inserts sample data into the sales table."""
    sample_data = [
        (10, "New York", "Product A", 1),
        (20, "London", "Product B", 2),
        (15, "New York", "Product C", 3),
        (25, "London", "Product A", 4),
        (12, "Paris", "Product B", 5),
        (18, "Paris", "Product C", 6),
    ]
    sql = "INSERT INTO sales (Price, LocationName, ProductName, ProductID) VALUES (%s, %s, %s, %s)"
    try:
        cursor.executemany(sql, sample_data)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        connection.rollback()  # Rollback changes if error occurs


@app.route("/")
def index():
    mydb = get_db_connection()
    if not mydb:
        return "Database connection error", 500  # Return error status code
    mycursor = mydb.cursor()

    create_sales_table(mycursor)
    # Only insert sample data if table is empty
    mycursor.execute("SELECT COUNT(*) FROM sales")
    if mycursor.fetchone()[0] == 0:
      insert_sample_data(mycursor, mydb)


    try:
        mycursor.execute("SELECT LocationName, COUNT(*) AS PriceCount FROM sales GROUP BY LocationName")
        data = mycursor.fetchall()

        graph_data = [{'x': [row[0] for row in data], 'y': [row[1] for row in data], 'type': 'bar'}]
        graphJSON = plotly.utils.PlotlyJSONEncoder().encode(graph_data)

        mycursor.close()
        mydb.close() # Close connection after usage
        return render_template("index.html", graphJSON=graphJSON)

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return "Error fetching data", 500

if __name__ == "__main__":
    app.run(debug=True)