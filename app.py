# app.py (Python - Flask and Streamlit integration)

from flask import Flask, render_template, redirect, url_for # Import url_for and redirect
import sqlite3
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import os

app = Flask(__name__)

# Database setup (using a more robust approach with try-except and parameterization)
DB_NAME = "sales_data.db"  # Use a variable for the database name


def create_and_populate_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                product TEXT,
                category TEXT,
                sales_quantity INTEGER,
                sales_amount REAL
            )
        ''')

        dummy_data = [
            ('Product A', 'Electronics', 100, 5000.00),
            ('Product B', 'Clothing', 50, 2500.00),
            ('Product C', 'Electronics', 75, 3750.00),
            ('Product D', 'Books', 120, 2400.00),
            ('Product E', 'Clothing', 90, 4500.00),
        ]

        cursor.executemany("INSERT OR IGNORE INTO sales VALUES (?, ?, ?, ?)", dummy_data)  # Parameterized query
        conn.commit()
    except Exception as e:  # Handle potential database errors
        print(f"Database error: {e}")
        conn.rollback()  # Rollback changes in case of error. 
    finally:
        conn.close()

# Call the function to create/populate the database on app start
create_and_populate_db()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    # Fetch data from SQLite (using a context manager)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            df = pd.read_sql_query("SELECT * FROM sales", conn)
    except Exception as e:  # Handle potential database query errors
        print(f"Error fetching data: {e}")
        st.error("Error fetching data. Please check logs.") # Display error message to user in Streamlit
        return redirect(url_for('index')) # Redirect back to main page on error



    st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:")

    selected = option_menu(None, ["Bar Chart", "Pie Chart"],
        icons=['bar-chart-fill', 'pie-chart-fill'],
        menu_icon="cast", default_index=0, orientation="horizontal")

    if selected == "Bar Chart":
        st.bar_chart(df, x="product", y="sales_amount")
    if selected == "Pie Chart":
        st.title("Sales Distribution by Category")
        category_sales = df.groupby("category")["sales_amount"].sum()
        st.pie_chart(category_sales)

    return st.markdown("Dashboard displayed!")  # Return a Streamlit element


if __name__ == '__main__':
    app.run(debug=True)  # In development, set debug=True. In production set debug=False.