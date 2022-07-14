import sqlite3

from flask_restful import Resource, reqparse


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

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'This field cannot be left blank'
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = 'This field cannot be left blank'
    )
    def post(self):
        data = UserRegister.parser.parse_args()

        if User.findByUsername(data['username']):
            return {'message': 'User with that username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = 'INSERT INTO users VALUES (Null,?,?)'
        cursor.execute(query, (data['username'], data['password'])) 

        connection.commit()

        connection.close()

        return {'message': 'User successfully created'}, 201