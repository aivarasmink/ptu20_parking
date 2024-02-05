import sqlite3

connection = sqlite3.connect("expenses.db")
cursor = connection.cursor()

def create_tables(
        connection: sqlite3.Connection = connection,
        cursor: sqlite3.Cursor = cursor,
    ):
    queries = [
        '''
CREATE TABLE IF NOT EXISTS expanses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME NOT NULL,
    category TEXT NOT NULL,
    amount DECIMAL(18,2) DEFAULT 0,
    description TEXT
);'''
    ]
    with connection:
        for query in queries:
            cursor.execute(query)

if __name__ == "__main__":
    create_tables()
