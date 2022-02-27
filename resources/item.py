# this is a CRUD API - Create Read Update Delete
# you could also have a Store resource that contains the below methods

# methods within a class should be separated by one new line
# classes within a file should be separated by two new lines

# json is a string in dictionary format and it's useful for sending
# data from one application to another
# for example, our javascript application might request a list of stores
# and they come back as a json and then we can look at each dictionary
# and retrieve some data from it just like we do in python
# json is not a dictionary, json is a long string of text so our
# application has to return a string in dictionary format and then
# javascript has to read that and deal with it as a string, maybe
# convert it to a javascript dictionary and then deal with it like that
# so there has to be some sort of conversion between a dictionary, which
# is a python thing and a string, which is something we can send over the
# internet, so we can't send a python dictionary to javascript because
# javascript wouldn't understand it but javascript does understand what
# text is and then it can do it's own conversion there
# flask has a method called jsonify which takes in a dictionary and
# converts it to json, which is a string in dictionary format

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# the Item class inherits from the Resource class
# which is imported from flask_restful at the top of this file
class Item(Resource):
    # the line below initialises a new object which we can use to pass
    # the request
    # an instance of the RequestParser class is placed into the parser
    # variable
    # the RequestParser class is part of reqparse which was imported from
    # flask_restful
    # we're going to run the request through it and see which items match
    # those that we define in the parser
    # the parser belongs to the Item class as opposed to one of the methods
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    # this is an end point for retrieving an item
    # the jwt_required decorator means we have to authenticate the user before
    # we can call the get method
    # this decorator can be placed above any method and it will require a
    # JSON Web Token and authorisation header to be executed
    @jwt_required()
    def get(self, name):
        # this searches for the item in the database
        # the item variable is intialised and calls
        # the find_by_name function as that function has been imported with
        # the ItemModel class from models.items
        # the find_by_name function returns an item object and then we call
        # json() method from that object
        # the json method will return a json representation of the model (item.py)
        # so any data this model retrieves from the database can be viewed by the
        # user using json
        # json is a string in dictionary format which can be read by javascript
        # jsonify takes in a python dictionary and converts it to json
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # this is an end point for creating the items
    # name can be passed from the end of the URL
    # or it can be passed through the JSON payload
    def post(self, name):
        # we call an instance of the find_by_name function and pass in the
        # name of the item being searched for as the argument
        # if the find_by_name function finds an item with that name
        # we don't want to create a new item with that name
        # so we just return a message stating that it already exists
        # we also return error code 400 as it was a bad request
        # if the item exists the if statement will end here
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # we need to call the Item's parser
        # the arguments that come through the JSON payload will be parsed and
        # the valid ones will be put in the data variable
        # we've only defined price so if there are any other arguments in the
        # JSON payload we won't see them
        # the name of the item is on the end of the URL, not in the JSON payload
        data = Item.parser.parse_args()

        # an instance of the ItemModel object is inserted into the item variable
        # the data received from the parser is in the arguments
        item = ItemModel(name, **data)

        try:
            # the item variable calls the save_to_db function
            item.save_to_db()
        except:
            # if an error occurs a message is printed with the code for
            # internal server error
            return {"message": "An error occurred when inserting the item."}, 500

        # in this case the client is Postman but it could be a web or mobile app
        # we need to tell the client we've created this item and added it to
        # our database
        # so we return item so the application knows this has happened
        # we use the code 201 to say something has been created
        # the item variable is returned and then we call
        # json() method from that object
        # the json method will return a json representation of the model (item.py)
        # so any data this model retrieves from the database can be viewed by the
        # user using json
        # json is a string in dictionary format which can be read by javascript
        # jsonify takes in a python dictionary and converts it to json
        # we use the code 201 to say something has been updated
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        # we need to call the Item's parser
        # the arguments that come through the JSON payload will be parsed and
        # the valid ones will be put in the data variable
        # we've only defined price so if there are any other arguments in the
        # JSON payload we won't see them
        # the name of the item is on the end of the URL, not in the JSON payload
        data = Item.parser.parse_args()

        # this searches for the item in the database
        # the item variable is intialised and calls
        # the find_by_name function as that function has been imported with
        # the ItemModel class from models.items
        item = ItemModel.find_by_name(name)

        if item is None:
            # if the above find_by_name function finds nothing a new
            # instance of the ItemModel class is inserted into the item
            # variable with the name of the item from the URL and the data
            # from the parser
            item = ItemModel(name, **data)
        else:
            # if the item exists then the price data from the parser is inserted
            # into price method in the item variable
            # the item variable is an instance of the ItemModel class
            # which has been imported from item.py in the models folder
            # the ItemModel class contains a variable called price
            # the price variable is a method that the ItemModel class passes
            # into SQLAlchemy and the price variable contains an instance
            # of the db variable which calls the Column method
            # the db variable is imported from db.py and it contains an instance
            # of the SQLAlchemy object
            item.price = data['price']
            item.store_id = data['store_id']
        # because this item is uniquely identified by it's ID
        # that means all we have to do is call the save_to_db function
        # and SQLAlchemy will update the item or insert a new item if it
        # doesn't exist
        item.save_to_db()
        # in this case the client is Postman but it could be a web or mobile app
        # we need to tell the client we've updated this item
        # so we return the item so the application knows this has happened
        # this doesn't check the item is in the database, it just returns
        # the data that was entered by the user
        # the item variable is returned and then we call
        # json() method from that object
        # the json method will return a json representation of the model (item.py)
        # so any data this model retrieves from the database can be viewed by the
        # user using json
        # json is a string in dictionary format which can be read by javascript
        # jsonify takes in a python dictionary and converts it to json
        # we use the code 201 to say something has been updated
        return item.json(), 201


# the ItemList class inherits from the Resource class
# which is imported from flask_restful at the top of this file
class ItemList(Resource):
    # this is an end point for retrieving all the items
    # it has a 'get' method as that's what we defined in the Postman collection
    # we didn't pass in any parameters in the Postman collection
    # so there's not going to be any parameters to the method other than self
    # self represents the instance of the class. By using the “self” keyword we
    # can access the attributes and methods of the class
    def get(self):
        # we use the SQLAlchemy query builder from the ItemModel object
        # the ItemModel object was imported at the top of this file
        # and it contains an instance of
        # the SQLAlchemy object which has a .all() method which returns all the
        # objects in the database
        # when the data is inserted into the database
        # it is passed to SQLAlchemy within an object and
        # SQLAlchemy can directly translate from object to row in a database
        # the below code translates to this SQL code:
        # SELECT * FROM items
        # we return a dictionary
        # the value of 'items' contains a list comprehension
        # the list comprehension states that for every object
        # returned by the .all() method from the database we return that object
        # in the variable
        # 'item', which is an instance of the ItemModel object, and call
        # the json() method from that instance of the ItemModel object
        # the ItemModel object returns each item in the database as an instance
        # of the ItemModel object
        # the ItemModel object inherited the json() method from the SQLAlchemy
        # object
        # the json method will return a json representation of the
        # ItemModel object so any data this object retrieves from the database
        # can be viewed by the user using json
        # json is a string in dictionary format which can be read by javascript
        return {'items': [item.json() for item in ItemModel.query.all()]}
