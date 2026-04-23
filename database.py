
import sqlite3

class Database:
    def __init__(self, db_name="watchlist.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS movies 
                               (id INTEGER PRIMARY KEY, user_id TEXT, title TEXT, 
                                genre TEXT, rating INTEGER, status TEXT)''')
        self.conn.commit()

    def query(self, sql, params=()):
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor