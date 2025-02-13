from flask import Flask, render_template
import mysql.connector
import json
import os

app = Flask(__name__)

# Get database credentials from environment variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER", "root")  # Default to root for local testing ONLY. NEVER in production.
DB_PASSWORD = os.environ.get("DB_PASSWORD", "nasa") # Extremely insecure default. Change this immediately!
DB_NAME = os.environ.get("DB_NAME", "sales_db")


@app.route('/')
def index():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT LocationName, COUNT(*) AS PriceCount FROM sales GROUP BY LocationName")
        data = mycursor.fetchall()
        labels = [row[0] for row in data]
        values = [row[1] for row in data]
        return render_template('index.html', labels=json.dumps(labels), values=json.dumps(values))
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Log the error for debugging
        return "Database error", 500 # Return a 500 error to the client
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mycursor.close()
            mydb.close()


if __name__ == '__main__':
    app.run(debug=True) # Never set debug=True in production