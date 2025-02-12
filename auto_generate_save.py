from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__)

EXCEL_FILE = os.environ.get("EXCEL_FILE", "your_excel_file.xlsx")  # Use environment variable for file path

# Load data outside the request handling to improve performance
try:
    df = pd.read_excel(EXCEL_FILE)
except FileNotFoundError:
    print(f"Error: File '{EXCEL_FILE}' not found.")
    exit()
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()


@app.route("/", methods=["GET", "POST"])
def index():
    columns = df.columns.tolist()
    selected_columns = request.form.getlist("columns") if request.method == "POST" else []
    chart_path = None
    error_message = None

    if request.method == "POST" and selected_columns:
        try:
            fig, ax = plt.subplots()  # Use plt.subplots for better figure/axes management
            for column in selected_columns:
                ax.plot(df.index, df[column], label=column)
            ax.legend()
            ax.set_title("Selected Columns Chart") # Add title for better clarity
            ax.set_xlabel("Index") # Label X-axis
            ax.set_ylabel("Values") # Label Y-axis


            # Save the plot to a temporary file
            chart_path = "static/chart.png"  # Store in static folder
            plt.savefig(chart_path)
            plt.close(fig) # Close the figure to free up memory

        except KeyError as e:
            error_message = f"Column not found: {e}"
        except Exception as e:
            error_message = f"An error occurred during plotting: {e}"

    return render_template("index.html", columns=columns, selected_columns=selected_columns, chart_path=chart_path, error=error_message)



if __name__ == "__main__":
    app.run(debug=True)