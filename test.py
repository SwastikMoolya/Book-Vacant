import sqlite3

def insert_example_data():
    # Connect to SQLite3 database
    conn = sqlite3.connect("bus_booking_system.db")
    cursor = conn.cursor()

    try:
        # Insert a sample user (passenger)
        cursor.execute(''' 
        INSERT INTO Users (name, email, password, role)
        VALUES ('John Doe', 'john@example.com', 'password123', 'passenger')
        ''')
        
        # Insert a sample bus owner
        cursor.execute(''' 
        INSERT INTO Users (name, email, password, role)
        VALUES ('Alice', 'alice@busowner.com', 'password123', 'bus_owner')
        ''')
        
        # Insert a sample bus with owner_id (we assume the bus owner has user_id 2)
        cursor.execute(''' 
        INSERT INTO Buses (bus_name, owner_id)
        VALUES ('City Express', 2)
        ''')

        # Get the bus_id of the newly inserted bus
        cursor.execute("SELECT bus_id FROM Buses WHERE bus_name = 'City Express'")
        bus_id = cursor.fetchone()[0]
        
        # Insert bus stops
        cursor.execute('''
        INSERT INTO Stops (bus_id, stop_name, stop_order, departure_time)
        VALUES (?, 'City A', 1, '2024-12-21 08:00:00'),
               (?, 'City B', 2, '2024-12-21 09:00:00'),
               (?, 'City C', 3, '2024-12-21 10:00:00')
        ''', (bus_id, bus_id, bus_id))

        # Commit changes to save bus and stops
        conn.commit()

        # Insert a sample reservation with seat number
        # First, retrieve all available seat numbers for the bus
        cursor.execute("SELECT seat_number FROM Reservations WHERE bus_id = ?", (bus_id,))
        reserved_seats = {row[0] for row in cursor.fetchall()}

        total_seats = 50
        available_seats = set(range(1, total_seats + 1)) - reserved_seats

        if not available_seats:
            print("No available seats.")
            return

        # Assign the first available seat
        seat_number = min(available_seats)

        # Insert a reservation for the passenger (assuming the passenger_id is 1)
        cursor.execute('''
        INSERT INTO Reservations (passenger_id, bus_id, start_stop, end_stop, seat_number)
        VALUES (?, ?, 'City A', 'City B', ?)
        ''', (1, bus_id, seat_number))

        conn.commit()
        print("Example data inserted successfully!")
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    insert_example_data()
