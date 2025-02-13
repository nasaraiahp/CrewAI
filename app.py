import os

from flask import Flask, render_template
import plotly.graph_objs as go
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

app = Flask(__name__)

# Database URL environment variable (more secure)
db_url = os.environ.get("DATABASE_URL")  # e.g., mysql+mysqlconnector://user:password@host:port/database

if not db_url:
    raise ValueError("DATABASE_URL environment variable not set")

# Create a SQLAlchemy engine with connection pooling
engine = create_engine(db_url, poolclass=QueuePool, pool_size=5, max_overflow=10, pool_pre_ping=True)


@app.route("/")
def index():
    try:
        with engine.connect() as connection:
            # Use parameterized query to prevent SQL injection
            query = text("SELECT LocationName, COUNT(*) AS PriceCount FROM sales GROUP BY LocationName")
            result = connection.execute(query)

            data = result.fetchall()  # Fetch all results at once for efficiency
            location_names = [row.LocationName for row in data]
            price_counts = [row.PriceCount for row in data]

        # Create the Plotly bar graph
        fig = go.Figure(data=[go.Bar(x=location_names, y=price_counts)])
        fig.update_layout(title="Price Count by Location", xaxis_title="Location Name", yaxis_title="Price Count")
        graphJSON = fig.to_json()

        return render_template("index.html", graphJSON=graphJSON)

    except Exception as e:
        # Log the error for debugging (don't display it directly in production)
        print(f"Error: {e}")  # Or use a proper logging library
        return "An error occurred", 500  # Return a generic error message to the user



if __name__ == "__main__":
    app.run(debug=False)  # Disable debug mode in production