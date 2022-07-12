import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

createTable = 'CREATE TABLE IF NOT EXISTS users (id int, username txt, password txt)'
cursor.execute(createTable)

connection.commit()

connection.close()
