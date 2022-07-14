import sqlite3
#from this import d
import hmac


connection = sqlite3.connect('data.db')

cursor = connection.cursor()

createTable = 'CREATE TABLE users (id int, username text, password text)'

cursor.execute(createTable)

user = (1, 'jose', 'asdf')

insertQuery = 'INSERT INTO users VALUES (?,?,?)'
cursor.execute(insertQuery, user)
    
users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz')

]
cursor.executemany(insertQuery, users)

selectQuery = 'SELECT * FROM users'
for row in cursor.execute(selectQuery):
    print(row)

connection.commit()

connection.close()

