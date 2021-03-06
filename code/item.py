import sqlite3
from turtle import update
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

class Item(Resource):
    """
    Class to hold the get and post command from individual items
    """
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank'
    )

    @jwt_required()
    def get(self, name:str):
        item = self.findByName(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def findByName(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name':row[0], 'price': row[1]}}

    def post(self,name:str):
        if self.findByName(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        
        data = self.parser.parse_args()
        
        item  = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {'message':'An error occured inserting the item'}, 500 #internal server error


        return item, 201
    
    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES (?,?)'
        cursor.execute(query, (item['name'],item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'item deleted'}

    def put(self, name):
        data = self.parser.parse_args()

        item = self.findByName(name)
        updatedItem = {'name': name, 'price': data['price']}
        if not item:
            try:
                self.insert(updatedItem)
            except:
               return {'message':'An error occured inserting the item'}, 500 
        else:
            try:
                self.update(updatedItem)
            except:
                return {'message':'An error occured updating the item'}, 500 
            

        return updatedItem

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (item['price'],item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items':items}