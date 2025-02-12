# create_db.py
import sqlite3
import random
import os

db_path = os.path.join(os.path.dirname(__file__), 'data.db')  # Use relative path for database

def create_database(db_path): # Wrap in a function for better organization and reusability
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            region TEXT,
            product TEXT,
            sales INTEGER
        )
    ''')

    regions = ['North', 'South', 'East', 'West']
    products = ['A', 'B', 'C', 'D']

    # Use executemany for more efficient batch insertion
    data = [(random.choice(regions), random.choice(products), random.randint(100, 1000)) for _ in range(50)]
    cursor.executemany("INSERT INTO sales (region, product, sales) VALUES (?, ?, ?)", data)

    conn.commit()
    conn.close()

if __name__ == "__main__":  # Ensure database creation only runs when script is executed directly
    create_database(db_path)



# generate_charts.py
import plotly.graph_objects as go
import sqlite3
import pandas as pd
import os

db_path = os.path.join(os.path.dirname(__file__), 'data.db') # Use relative path
charts_dir = "charts"  # Store chart directory name in a variable
os.makedirs(charts_dir, exist_ok=True) # Ensure charts directory exists

def generate_charts(db_path, charts_dir): # Wrap in a function

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * from sales", conn)
    conn.close()


    def create_and_save_chart(fig, filename):
        filepath = os.path.join(charts_dir, filename) # Use os.path.join
        fig.write_html(filepath)


    # Chart 1: Bar chart of total sales by region
    # Use aggregation directly in the query for better performance
    fig1 = go.Figure(data=[go.Bar(x=df.groupby('region')['sales'].sum().index, y=df.groupby('region')['sales'].sum().values)])
    fig1.update_layout(title_text="Total Sales by Region")
    create_and_save_chart(fig1, "chart1.html")

    # ... (rest of the chart generation code is the same, using create_and_save_chart)

if __name__ == "__main__":
    generate_charts(db_path, charts_dir)


# dashboard.html (No changes required)