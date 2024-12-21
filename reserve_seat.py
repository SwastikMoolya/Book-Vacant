import sqlite3

def reserve_seat(passenger_id, bus_id, start_stop, end_stop):
    # Connect to SQLite3 database
    conn = sqlite3.connect("bus_booking_system.db")
    cursor = conn.cursor()

    try:
        # Check if the bus has the specified stops
        cursor.execute("SELECT stop_name FROM Stops WHERE bus_id = ? ORDER BY stop_order", (bus_id,))
        stops = [row[0] for row in cursor.fetchall()]
        
        if start_stop not in stops or end_stop not in stops:
            print("Invalid stops.")
            return

        start_index = stops.index(start_stop)
        end_index = stops.index(end_stop)
        
        if start_index >= end_index:
            print("Invalid stop order.")
            return

        # Check for available seat numbers for the bus
        cursor.execute('''SELECT seat_number FROM Reservations WHERE bus_id = ?''', (bus_id,))
        reserved_seats = {row[0] for row in cursor.fetchall()}

        # Assuming there are 50 seats per bus, you can adjust this as needed
        total_seats = 50
        available_seats = set(range(1, total_seats + 1)) - reserved_seats

        if not available_seats:
            print("No available seats on this bus.")
            return

        # Assign the first available seat
        seat_number = min(available_seats)

        # Insert reservation with seat number
        cursor.execute(''' 
        INSERT INTO Reservations (passenger_id, bus_id, start_stop, end_stop, seat_number)
        VALUES (?, ?, ?, ?, ?)
        ''', (passenger_id, bus_id, start_stop, end_stop, seat_number))

        conn.commit()
        print(f"Seat {seat_number} reserved successfully!")
    except sqlite3.Error as e:
        print(f"Error reserving seat: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Example usage
    reserve_seat(passenger_id=2, bus_id=1, start_stop="City B", end_stop="City C")
