import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserManager:
    def __init__(self):
        self.connection = sqlite3.connect('lychee.db')
        self.cursor = self.connection.cursor()

    def register_user(self, username, password):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.connection.commit()

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def close(self):
        self.connection.close()
