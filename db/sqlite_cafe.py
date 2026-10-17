import os
import sqlite3

# Sources used for syntax and understanding different concepts of SQLite https://docs.python.org/3.13/library/sqlite3.html#, https://www.sqlitetutorial.net/

class SQLiteCafe:
    def __init__(self,filename,table, columns):
        sqlite_dir = os.environ.get("SQLITE_DIR", "data")
        self.path = os.path.join(sqlite_dir, filename)
        self.table = table
        self.columns = columns

    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

# Lists all items from database
    def list_all(self):
        with self._connect() as conn:
            rows = conn.execute(f"SELECT * FROM {self.table} ORDER BY id").fetchall()
        return [dict(row) for row in rows]

# Fetches one item from database
    def get(self, item_id):
        with self._connect() as conn:
            row = conn.execute(f"SELECT * FROM {self.table} WHERE id = ?", (item_id,)).fetchone()
        return dict(row) if row else None

# Adds one item to the database
    def add(self, data):
        colms = ", ".join(self.columns)
        mark = ", ".join("?" for _ in self.columns)
        vals = [data[c] for c in self.columns]
        with self._connect() as conn:
            cursor = conn.execute(f"INSERT INTO {self.table} ({colms}) VALUES ({mark})", vals)
        return cursor.lastrowid

# Updates existing item in database
    def update(self, item_id, data):
        tasks = ", ".join(f"{c} = ?" for c in self.columns)
        vals = [data[c] for c in self.columns] + [item_id]
        with self._connect() as conn:
            conn.execute(f"UPDATE {self.table} SET {tasks} WHERE id = ?", vals)

# Deletes item from database
    def delete(self, item_id):
        with self._connect() as conn:
            conn.execute(f"DELETE FROM {self.table} WHERE id = ?", (item_id,))



cafe_menu = SQLiteCafe(
    "menu.db", "items", ["name", "category", "price", "in_stock"]
)

cafe_staff = SQLiteCafe(
    "staff.db", "staff_persons", ["name", "role", "hourly_wage", "starting_date"]
)