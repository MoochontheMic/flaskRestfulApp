import sqlite3
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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES (?,?)'
        cursor.execute(query, (item['name'],item['price']))

        connection.commit()
        connection.close()

        return item, 201
    
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

        item = next(filter(lambda x: x['name']== name ,items), None)
        if not item:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}