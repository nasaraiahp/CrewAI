from flask import Flask, request, jsonify
import mysql.connector  # Or your preferred database connector

app = Flask(__name__)

# Database connection details (replace with your credentials)
db_config = {
    "user": "your_db_user",
    "password": "your_db_password",
    "host": "your_db_host",
    "database": "your_db_name"
}

@app.route('/your-data-endpoint', methods=['POST'])
def get_data():
    query = request.json.get('query')
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)  # Use dictionary=True for named results
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error as JSON
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()

if __name__ == '__main__':
    app.run(debug=True)