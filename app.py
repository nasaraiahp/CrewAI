import sqlite3
import matplotlib.pyplot as plt
import os

db_path = 'sales_data.db'  # Define database path

# Use a context manager for better resource management
with sqlite3.connect(db_path) as conn:  # Use file-based DB for persistence
    with open('create_table_and_insert.sql', 'r') as sql_file:
        conn.executescript(sql_file.read())
    cursor = conn.cursor()

    queries = [
        # ... (queries remain the same)
    ]
    chart_titles = [
        # ... (chart titles remain the same)
    ]

    chart_dir = "charts"  # Store directory name in a variable
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)


    for i, query in enumerate(queries):
        cursor.execute(query)
        results = cursor.fetchall()
        # Handle empty result set
        if not results:
            print(f"No data found for query {i+1}. Skipping chart generation.")
            continue

        labels = [row[0] for row in results]
        values = [row[1] for row in results]

        plt.figure(figsize=(8, 6))
        plt.bar(labels, values)
        plt.title(chart_titles[i])
        plt.xlabel(labels[0].split()[0])
        plt.ylabel('Sales' if any('Sales' in val for val in map(str, values)) else 'Average Sales')  # Simpler y-axis label logic
        plt.savefig(os.path.join(chart_dir, f"chart{i+1}.png"))  # Use os.path.join for platform independence
        plt.close()

# Connection is closed automatically by the context manager