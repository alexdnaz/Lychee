import sqlite3

# Connect to the database (or create it if it doesn't exist)
connection = sqlite3.connect('lychee.db')
cursor = connection.cursor()

# SQL schema to create the necessary tables
schema = """
-- Create a table for categories
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Create a table for articles
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- Create a table for votes
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER,
    vote INTEGER NOT NULL, -- 1 for approval, 0 for rejection
    user_id INTEGER, -- Optional: To track who voted, if you have a user management system
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles (id)
);
"""

# Execute the schema to create the tables
cursor.executescript(schema)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database and tables created successfully!")
