# create_db.py
import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'sales.db')  # Use os.path.join for platform compatibility
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_data (
            region TEXT,
            product TEXT,
            sales INTEGER,
            month INTEGER,
            year INTEGER
        )
    ''')

    data = [
        ('North', 'Product A', 1000, 1, 2024),
        ('North', 'Product B', 1500, 1, 2024),
        # ... (rest of the data)
    ]

    cursor.executemany("INSERT INTO sales_data VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()

except sqlite3.Error as e: # Handle potential database errors
    print(f"Database error: {e}")
    conn.rollback() # Rollback changes if error occurs
finally:
    conn.close() # Ensure connection is closed

# (Optional) Web server code -  Move this to a separate file (e.g., server.py)
#  In a real application, use a production-ready web framework (Flask, Django, etc.)
if __name__ == "__main__":  # Only run the server when script is executed directly
    import http.server
    import socketserver
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()