import sqlite3

def add_bus(owner_id, bus_name, stops_with_departure_time_with_charge):
    # Connect to SQLite3 database
    conn = sqlite3.connect("bus_booking_system.db")
    cursor = conn.cursor()

    try:
        # Add bus details (without start_city and destination_city)
        cursor.execute('''
        INSERT INTO Buses (bus_name, owner_id)
        VALUES (?, ?)
        ''', (bus_name, owner_id))
        bus_id = cursor.lastrowid

        # Add stops to the Stops table with departure_time and charges
        for order, (stop, departure_time, charge) in enumerate(stops_with_departure_time_with_charge, start=1):
            cursor.execute('''
            INSERT INTO Stops (bus_id, stop_name, stop_order, departure_time, charge)
            VALUES (?, ?, ?, ?, ?)
            ''', (bus_id, stop, order, departure_time, charge))

        conn.commit()
        print("Bus and stops added successfully with charges!")
    except sqlite3.Error as e:
        print(f"Error adding bus: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Example usage with charges for each stop
    add_bus(owner_id=1, bus_name="City Express", stops_with_departure_time_with_charge=[
        ("City A", "2024-12-21 08:00:00", 0.0),
        ("City B", "2024-12-21 09:00:00", 10.0),
        ("City C", "2024-12-21 10:00:00", 15.0),
        ("City D", "2024-12-21 11:00:00", 20.0)
    ])
