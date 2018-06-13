from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)# endpoint : /auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):#next returns the first item in the matched list
        return {'item': next(filter(lambda x: x['name'] == name, items), None)}
                             #filter filters the items (using a function, list, return none if nothing filters )
    def post(self, name):#add item
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args() #takes is data from the client and parses the argument to ignore un-intended data

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item

    @jwt_required()
    def delete(self, name):#delete an item
        global items
        items = list(filter(lambda x: x['name'] != name, items)) #creates a new list but without the item
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):#update an item
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):# (ItemList, '/items') #to return all the items
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>') #to do operations on specific items
api.add_resource(ItemList, '/items') #to return all the items
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
