import sqlite3 as sql

db = 'test.db'

stmt = "CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)"
with sql.connect(db) as conn:
    cursor = conn.cursor()
    cursor.execute(stmt)
    conn.commit()

stmt = "ALTER TABLE test ADD COLUMN 'PROUT' TEXT"
with sql.connect(db) as conn:
    cursor = conn.cursor()
    cursor.execute(stmt)
    conn.commit()


stmt = "INSERT INTO test (name) values ('toto')"
with sql.connect(db) as conn:
    cursor = conn.cursor()
    res = cursor.execute(stmt)
    conn.commit()
    print(cursor.rowcount)
    print(cursor.lastrowid)