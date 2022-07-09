import sqlite3

from colorama import Cursor



class User:
    """
    Creates/initiaises a user for the system
    """
    def __init__(self, iD:int, username:str, password:str):
        self.id = iD
        self.username = username
        self.password = password

    @classmethod
    def findByUsername(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)

        else:
            user = None
        
        connection.close()

        return user

    @classmethod
    def findById(cls, iD):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(query, (iD,))
        row = result.fetchone()
        if row:
            user = cls(*row)
            
        else:
            user = None
        
        connection.close()

        return user
