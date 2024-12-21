import sqlite3
from tabulate import tabulate  # Install tabulate via pip if not already installed: pip install tabulate

# Connect to SQLite3 database
conn = sqlite3.connect("bus_booking_system.db")
cursor = conn.cursor()

# Function to fetch and display data from a table
def display_table_data(table_name):
    try:
        # Get the column names for the table
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        # Fetch the table data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Print the table name and the column names with the data
        print(f"\nData from {table_name} table:")
        if rows:
            print(tabulate(rows, headers=columns, tablefmt="pretty"))
        else:
            print("No data found.")
    except sqlite3.Error as e:
        print(f"Error fetching data from {table_name}: {e}")

# Display data from all tables
def display_all_data():
    tables = ["Users", "Buses", "Stops", "Reservations"]
    for table in tables:
        display_table_data(table)

# Main script to execute
if __name__ == "__main__":
    display_all_data()

# Close the database connection
conn.close()
