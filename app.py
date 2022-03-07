from flask import Flask
# we need to use flask_restful for our API mappings (functions that connect
# our API to a database)
from flask_restful import Api
# we need to use flask_jwt for authentication
# we need to import JSON Web Token
# it's a proposed Internet standard for creating optional signature/encryption
# whose payload holds JSON that asserts some number of claims
from flask_jwt import JWT
# from security.py we need to import the authenticate and identity methods
from security import authenticate, identity
# from resources/user.py we need to import the UserRegister class,
# which is our resource
from resources.user import UserRegister
# from resources/item.py we need to import the Item class and ItemList class
from resources.item import Item, ItemList
# from resources/store.py we need to import the Store class and StoreList class
from resources.store import Store, StoreList
# from db.py we need to import the db variable which contains an instance
# of the SQLAlchemy object
from db import db

app = Flask(__name__)
# we need to specify a configuration property because in order to know when
# an object had changed but had not been saved to the database, the extension,
# flask_sqlalchemy (which we imported SQLAlchemy from), was tracking every
# change we made to the SQLAlchemy session
# and that took some resources, so know we're turning it off because the
# SQLAlchemy library has it's own modification tracker, which is a bit better,
# so this turns off the flask_sqlalchemy modification tracker but not the
# SQLAlchemy modification tracker and it's only changing the
# behaviours of the flask_sqlalchemy extension and not the underlying
# SQLAlchemy behaviour
# SQLAlchemy is an open-source SQL toolkit
# flask_sqlalchemy is an extension for Flask that adds support for SQLAlchemy
# to an application
# we need to tell SQLAlchemy where to find the database so we say it lives
# at the root folder of our project
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'fo53?c\RT29&'
api = Api(app)

# we initialise the JWT object by
# creating the jwt variable and placing in it an instance of
# the JWT class with 3 arguments which are app.py, the authenticate
# function and the identity function
# this will allow for authentication of the users as the JWT class
# creates a new end point which is /auth
# when we call /auth we send it a username and a password which
# the JWT class sends to the authenticate function
# if the authenticate function returns the username after verifying the
# username and password then the auth endpoint returns a JSON Web Token
# which we can send to the next request we make which will call the identity
# function
jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
# below is the Item resource
# for example, the URL could be http://127.0.0.1:5000/item/Item1
# the name Item1 goes into the 'name' parameter
# we no longer have to do the decorator ourselves
api.add_resource(Item, '/item/<string:name>')
# the end point for the ItemList resource is ''/items'
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
# the end point for the UserRegister resource is '/register'
# so when we execute a post request to /register that will call the UserRegister
# which will call the post method
api.add_resource(UserRegister, '/register')

# you don't need to enter port=5000 as that's the default
# also if an object is imported from this file before the app has started running
# we don't want the app to start running so we include the code below to
# prevent that as the below name is assigned to this file when this file runs
# as when an object is imported from a file python checks the code in that file
# and runs some of the code
# if the name of this file isn't main then it means we have imported it and
# don't want to run it
if __name__== '__main__':
    # we'll call the init_app method on the db variable and pass in the app
    # variable as a parameter as the app variable contains an instance of our
    # flask app
    db.init_app(app)
    app.run(port=5000, debug=True)
