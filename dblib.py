import sqlite3

class GradeBookDatabase:

    def __init__(self, db_name="gradebook.db"):
        self.db_name = db_name

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS GradeBook (
                    gid    INTEGER PRIMARY KEY AUTOINCREMENT,
                    fname  TEXT,
                    lname  TEXT,
                    grade  INTEGER
                );
            """)

    def fill_data(self):
        data = [('Melissa', 'Bishop', 70),
                ('Linda', 'Scanlon', 55),
                ('Russel', 'Gruver', 60),
                ('Maria', 'Mayes', 100),
                ('Dennis', 'Hill', 95),
                ('Nathan', 'Martin', 40),
                ('William', 'Biggs', 85),
                ('Lois', 'Ballard', 60),
                ('Larry', 'Manning', 50),
                ('Dustin', 'Smalls', 30),
                ('Alice', 'Lucas', 70),
                ('John', 'Howell', 90)]

        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM GradeBook") # Clean database
            cur.executemany("INSERT INTO GradeBook(fname, lname, grade) VALUES(?, ?, ?)", data)

    def save_grade(self, fname, lname, grade):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO GradeBook(fname, lname, grade) VALUES(?, ?, ?)", (fname, lname, grade))

    def get_grades(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM GradeBook")
            return cur.fetchall()

    def get_count_and_average(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*), AVG(grade) FROM GradeBook")
            return cur.fetchone()

    def delete_grade(self, gid):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM GradeBook WHERE gid=?", (gid, ))

    def update_grade(self, gid, fname, lname, grade):
        pass


if __name__ == '__main__':
    db = GradeBookDatabase()
    db.create_table()
    db.fill_data()
    print("Database initialized.")