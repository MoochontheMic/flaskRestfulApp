from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth


items = []

class Item(Resource):
    """
    Class to hold the get and post command from individual items
    """
    @jwt_required()
    def get(self, name:str):
        item = next(filter(lambda x:(x['name'] == name), items), None)
        return {'item': item}, 200 if item else 404

    def post(self,name:str):

        if next(filter(lambda x:(x['name'] == name), items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = request.get_json(force=True)
        item  = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))

class ItemList(Resource):
    def get(self):
        return {'items': items}


    

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
