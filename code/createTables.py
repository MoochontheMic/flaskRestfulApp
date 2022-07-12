import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

createTable = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username txt, password txt)'
cursor.execute(createTable)

createTable = 'CREATE TABLE IF NOT EXISTS items (name txt, price real)'
cursor.execute(createTable)

connection.commit()

connection.close()
