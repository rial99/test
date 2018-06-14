import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):#next returns the first item in the matched list
        item = self.find_by_name(name)
        if item:
            return item
        return {'message':'item not found'}, 404
                             #filter filters the items (using a function, list, return none if nothing filters )



    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name':row[0],'price':row[1]}}


    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query,(item['name'],item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'],item['name']))

        connection.commit()
        connection.close()


    def post(self, name):#add item
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args() #takes is data from the client and parses the argument to ignore un-intended data

        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {'message':'an error occured towards inserting the item'}, 500

        return item, 201




    @jwt_required()
    def delete(self, name):#delete an item
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query,(name,))

            connection.commit()
            connection.close()
            return {'message':'item deleted'}

        return {'message':'no such item exist'}


    @jwt_required()
    def put(self, name):#update an item
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = self.find_by_name(name)
        updated_item = {'name':name,'price':data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message':'an error occured inserting the item'},500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message':'an error occured updating the item'},500
        return item




class ItemList(Resource):# (ItemList, '/items') #to return all the items
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []

        for row in result:
            items.append({'name':row[0],'price':row[1]})

        connection.close()

        return {'items':items}
