import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from flask import Flask, render_template
import os

# --- Configuration ---
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "sales_data.db")  # Store DB in the same directory
SAMPLE_DATA = [
    ('Product A', 'Electronics', 1500),
    ('Product B', 'Clothing', 800),
    ('Product C', 'Electronics', 1200),
    ('Product D', 'Books', 500),
    ('Product E', 'Clothing', 900),
]


# --- Database Management ---
def create_connection(db_file):
    """Creates a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection error: {e}")
        return None

def create_table(conn):
    """Creates the sales table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                product TEXT,
                category TEXT,
                sales_amount REAL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error creating table: {e}")


def insert_sample_data(conn, data):
    """Inserts sample data into the sales table if it's empty."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales")
        if cursor.fetchone()[0] == 0:  # Check if table is empty
            cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", data)
            conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error inserting sample data: {e}")


# --- Flask setup (if needed for more complex backend operations later) ---
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

# --- Streamlit App ---
st.title("Sales Dashboard")

# --- Data Loading and Caching ---
@st.cache_data  # Cache the data
def load_data(conn):
    df = pd.read_sql_query("SELECT * from sales", conn)
    return df

# --- Database initialization happens outside cached function ---
conn = create_connection(DATABASE_PATH)
if conn:
    create_table(conn)
    insert_sample_data(conn, SAMPLE_DATA)
    df = load_data(conn)   # Call after the table has been populated
    conn.close()  # Close connection after loading


# --- Visualization ---
if df is not None: # Check if the dataframe was loaded
    st.subheader("Sales by Product")
    fig_bar = px.bar(df, x='product', y='sales_amount', color='category')
    st.plotly_chart(fig_bar)

    st.subheader("Sales Distribution by Category")
    category_sales = df.groupby('category')['sales_amount'].sum().reset_index()
    fig_pie = px.pie(category_sales, values='sales_amount', names='category')
    st.plotly_chart(fig_pie)
else:
    st.error("Could not load sales data.")  # Informative message


# Streamlit app run (if not using Flask)
if __name__ == '__main__' and not st._is_running_with_streamlit:  # Check Streamlit context
    st.set_option('server.headless', True)
    st.run()


# --- Uncomment to serve via Flask ---
# if __name__ == '__main__':
#     app.run(debug=True)