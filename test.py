import sqlite3

def test_connection():
    """Tests a connection to the SQLite database and prints a message."""
    try:
        # Connect to the database (replace 'your_database.db' with your actual database file)
        conn = sqlite3.connect('lychee.db') 
        print("Connected to SQLite database successfully!")
        print("Hello, World!")  # Print your message
        conn.close()  # Close the connection
    except sqlite3.Error as error:
        print(f"Error connecting to SQLite database: {error}")

if __name__ == "__main__":
    test_connection()

