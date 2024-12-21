import sqlite3

def create_tables():
    # Connect to SQLite3 database (or create it if it doesn't exist)
    conn = sqlite3.connect("bus_booking_system.db")
    cursor = conn.cursor()

    # Drop existing tables to reflect new changes (for development purposes, not in production)
    cursor.execute('''DROP TABLE IF EXISTS Users''')
    cursor.execute('''DROP TABLE IF EXISTS Buses''')
    cursor.execute('''DROP TABLE IF EXISTS Stops''')
    cursor.execute('''DROP TABLE IF EXISTS Reservations''')

    # Create tables
    # Table to store user details
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('passenger', 'bus_owner')) NOT NULL
    );
    ''')

    # Table to store bus details
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Buses (
        bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_name TEXT NOT NULL,
        owner_id INTEGER NOT NULL,
        FOREIGN KEY(owner_id) REFERENCES Users(user_id)
    );
    ''')

    # Table to store bus stops with departure_time and charges for each stop (to the next stop)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stops (
        stop_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_id INTEGER NOT NULL,
        stop_name TEXT NOT NULL,
        stop_order INTEGER NOT NULL,
        departure_time TIMESTAMP NOT NULL,
        charge REAL NOT NULL,  -- Charge from this stop to the next stop
        FOREIGN KEY(bus_id) REFERENCES Buses(bus_id)
    );
    ''')

    # Table to store seat reservations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_id INTEGER NOT NULL,
        bus_id INTEGER NOT NULL,
        start_stop TEXT NOT NULL,
        end_stop TEXT NOT NULL,
        seat_number INTEGER NOT NULL,
        reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(passenger_id) REFERENCES Users(user_id),
        FOREIGN KEY(bus_id) REFERENCES Buses(bus_id)
    );
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database setup completed successfully.")

if __name__ == "__main__":
    create_tables()
