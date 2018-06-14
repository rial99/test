from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

#all the imports for the endpoints
from security import authenticate, identity # /auth
from user import UserRegister # /register
from item import Item, ItemList # /item/<string:name>

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)# endpoint : /auth

api.add_resource(ItemList, '/items') #to return all the items
api.add_resource(Item, '/item/<string:name>') #to do operations on specific items
api.add_resource(UserRegister,'/register')


#class UserRegister(Resource):


if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
