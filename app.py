# app.py
import os
from flask import Flask, render_template
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)

# Get database credentials from environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


@app.route("/")
def index():
    mydb = get_db_connection()
    if mydb:
        try:
            mycursor = mydb.cursor()
            mycursor.execute("""
                SELECT Location_Name, COUNT(*) AS Price_Count, AVG(Price) AS Average_Price
                FROM sales
                GROUP BY Location_Name;
            """)
            data = mycursor.fetchall()
            labels = [row[0] for row in data]
            counts = [row[1] for row in data]
            average_prices = [row[2] for row in data]
            return render_template("index.html", labels=labels, counts=counts, average_prices=average_prices)

        except mysql.connector.Error as err:
            print(f"Database query error: {err}")
            return "Database query error", 500
        finally:
            mycursor.close()
            mydb.close() # Close the connection
    else:
        return "Database connection error", 500




if __name__ == "__main__":
    app.run(debug=False) #important change, change from True to False