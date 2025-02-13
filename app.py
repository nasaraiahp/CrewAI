import sqlite3
import plotly.express as px
import pandas as pd

# Database file name
DATABASE_FILE = 'sales_data.db'

# Function to generate and save the graph
def generate_sales_graph(db_file):
    try:
        # Use a context manager for database connection
        with sqlite3.connect(db_file) as conn:
            # Read data from the sales table
            sales_df = pd.read_sql_query("SELECT * from sales", conn)

        # Generate Price Count vs Location Name graph
        location_price_count = sales_df.groupby('LocationName')['Price'].count().reset_index()
        fig = px.bar(location_price_count, x='LocationName', y='Price', title='Price Count vs. Location Name')

        # Save graph as HTML file
        fig.write_html("price_count_by_location.html")

        print("Graph generated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    generate_sales_graph(DATABASE_FILE)