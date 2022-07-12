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
        item = next(filter(lambda x:(x['name'] == name), items), None)
        return {'item': item}, 200 if item else 404

    def post(self,name:str):
        if next(filter(lambda x:(x['name'] == name), items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        
        data = self.parser.parse_args()
        
        item  = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
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