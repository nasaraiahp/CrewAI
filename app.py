from flask import Flask, render_template, jsonify  # Import jsonify
import pandas as pd
import os
import random

app = Flask(__name__)

# Configuration (Better to move these to a config file or environment variables)
EXCEL_FILE = os.environ.get("EXCEL_FILE") or 'your_excel_file.xlsx'
ALLOWED_CHART_TYPES = ["bar", "line", "pie", "scatter", "doughnut"]


def create_chart_data(df, chart_type, x_col, y_col, title):
    """Helper function to prepare chart data."""
    if chart_type not in ALLOWED_CHART_TYPES:
        raise ValueError("Invalid chart type")

    if chart_type in ["pie", "doughnut"]:
        labels = df[x_col].tolist()
        data = df[y_col].tolist()
        chart_data = {
            "labels": labels,
            "datasets": [{"data": data, "backgroundColor": generate_colors(len(data))}]
        }
    else:
        labels = df[x_col].tolist()
        data = df[y_col].tolist()
        chart_data = {
            "labels": labels,
            "datasets": [{"label": title, "data": data, "borderColor": 'rgb(75, 192, 192)', "tension": 0.4}]
        }
    return chart_data


def generate_colors(num_colors):
    """Generate a list of random hex colors"""
    return ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(num_colors)]


@app.route('/chart_data')
def chart_data():
    """API endpoint to provide chart data as JSON."""
    try:
        df = pd.read_excel(EXCEL_FILE)

        # Example data (adapt as needed). Important: Don't hardcode column names in production.
        # Allow users to specify them (e.g., via query parameters) and validate user input.
        chart_data = {
            'chart1': create_chart_data(df, 'line', 'Column1', 'Column2', 'Chart 1 Title'),
            'chart2': create_chart_data(df, 'bar', 'Column3', 'Column4', 'Chart 2 Title'),
            'chart3': create_chart_data(df, 'pie', 'Column5', 'Column6', 'Chart 3 Title'),
            'chart4': create_chart_data(df, 'scatter', 'Column7', 'Column8', 'Chart 4 Title'),  # Corrected spelling here
            'chart5': create_chart_data(df, 'doughnut', 'Column9', 'Column10', 'Chart 5 Title')
        }
        return jsonify(chart_data)  # Return data as JSON

    except FileNotFoundError:
        return jsonify({'error': 'Excel file not found'}), 404  # Return 404 error
    except ValueError as e:  # Handle invalid chart type
        return jsonify({'error': str(e)}), 400 # 400 Bad Request for user errors
    except Exception as e:  # Catch other exceptions
        return jsonify({'error': 'An internal server error occurred'}), 500 # 500 for server errors


@app.route('/')
def dashboard():
    return render_template('dashboard.html')  # No need to pass data here


if __name__ == '__main__':
    app.run(debug=True)  # NEVER set debug=True in production