import sqlite3
# from db.py we need to import the db variable which contains an instance
# of the SQLAlchemy object
from db import db

# the UserModel class isn't a resource as the API can't receive data into this
# class or send this class as a JSON representation
# this class interacts with the database (the back end) but not the API
# (the front end)
# this class is a helper that we use to store some information about the user
# it's also a helper that contains some methods that allow us to easily retrieve
# user objects from a database
# this class is a model, which is our internal representation of an entity
# whereas a resource is the external representation of an entity
# our API clients like a website or a mobile app think they're interacting with
# resources
# the model is a helper that gives us more flexibility in our program without
# poluting the resource, which is what the clients interact with

# both the UserModel class and the ItemModel class are going to extend db.Model
# (receive db.Model as an argument)
# and that's going to tell the SQLAlchemy entity that the ItemModel class and
# the UserModel class are things we're going to be saving to and retrieving
# from a database, so it's going to create that mapping between the database
# and these objects

# this UserModel object is an API but not a REST API
# it exposes two endpoints(methods) which are find_by_username and find_by_id
# they are an interface for other parts of our program to interact with the user
# if the content of these functions changes that doesn't affect the other files
# that use them such as security.py as long as they still work
# similarly, with our REST API it doesn't matter if it's written in python or
# another language as long as the application using the API gets the information
# it requested in the format it expects
class UserModel(db.Model):
    # we need to tell SQLAlchemy that the table in the database that data from
    # this class will be stored in is the users table
    __tablename__ = 'users'

    # A function is a piece of code that is called by name. It can be passed
    # data to operate on (i.e. the parameters) and can optionally return data
    # (the return value). All data that is passed to a function is explicitly
    # passed.
    # A method is a piece of code that is called by a name that is associated
    # with an object. In most respects it is identical to a function except for
    # two key differences:
    # A method is implicitly passed the object on which it was called.
    # A method is able to operate on data that is contained within the class
    # (remembering that an object is an instance of a class - the class is the
    # definition, the object is an instance of that data).

    # we need to tell SQLAlchemy which columns in the database this model
    # (the UserModel class) will be using,
    # so we initialise a variable called id and place in it an
    # instance of the db variable which calls the Column method
    # the parameters of the Column method are an instance of the db variable
    # which calls the Integer method (the datatype of that column) and a
    # variable called primary_key which contains the boolean value True,
    # meaning this column is the primary key, which means it contains unique
    # values and it's going to create an index based on it so it's easy to
    # search based on id
    # the variable can be called id as we're not using the python built-in id
    # method
    id = db.Column(db.Integer, primary_key=True)
    # the username column must contain strings of up to 80 characters
    username = db.Column(db.String(80))
    # the password column must contain strings of up to 80 characters
    password = db.Column(db.String(80))

    # this is an __init__() method
    # it creates an empty object which is the initial state of the class
    # it contains 4 arguments - self, _id, username and password
    # we use _id as id is a python keyword
    def __init__(self, username, password):
        # below are 2 instance variables unique to each instance
        # they are properties of this object and in order for the values
        # they contain to be saved in the database they must have the same names
        # as the database columns defined above
        # the model can have other properties with other names but the values
        # they contain won't be saved into or received from the database
        # the id column is automatically generated when the database is created
        # and it is autoincrementing so we don't need to create it here 
        self.username = username
        self.password = password

    # the save_to_db function has an instance of this current model as an argument
    # as when a resource calls this function they will pass data
    # into this model if the data needs to be inserted into the database
    # this save_to_db method saves the model to the database
    # SQLAlchemy can directly translate from object to row in a database
    # so we don't have to tell it what row to insert the data into
    # when we retrieve an object from the database that has a particular ID
    # then we can change the object's name and all we have to do is add it to
    # the session and commit it again and SQLAlchemy will do an update instead
    # of an insert so the save_to_db method can be used for insert and update
    def save_to_db(self):
        # we call the session method from the SQLAlchemy object
        # we call the add function from within the session method
        # we pass in an instance of this current model as an argument
        db.session.add(self)
        # as it's a db.session we can add more than one object if we want
        db.session.commit()

    # the find_by_username method will find the user in the database
    # it's the mapping on the username field in the database
    # it takes in the username field as an argument
    # mapping is the process of using a map (a higher-order function) that
    # either takes in one or more functions as arguments or returns a function
    # as a result
    # we include the cls (class) argument as the method needs that to interact with
    # the user object (class) and the username argument is what we search for
    # in the database
    # cls means we're using the current class, which is User, as opposed to
    # hardcoding the class name, which is helpful if we change the class name
    # in the future
    # SQLAlchemy allows us to easily map objects to database rows
    # that means we can use a map (a higher-order function) to allow an object
    # to interact with database rows
    @classmethod
    def find_by_username(cls, username):
        # the below code translates to this SQL code:
        # SELECT * FROM items WHERE username=username
        # a UserModel object will be returned
        # cls.query is the query builder object which allows us to build queries
        # first() gets the first row and SQLAlchemy converts it to a UserModel
        # object
        return cls.query.filter_by(username=username).first()

    # this method will find the user in the database
    # it's the mapping on userid
    # we include the self argument as the method needs that to interact with
    # the user object and the id argument is what we search for
    # if we use the classmethod decorator we use the cls argument instead
    # of the self argument
    # that means we're using the current class, which is User, as opposed to
    # hardcoding the class name, which is helpful if we change the class name
    # in the future
    @classmethod
    def find_by_id(cls, _id):
        # the below code translates to this SQL code:
        # SELECT * FROM items WHERE id=_id
        # a UserModel object will be returned
        # cls.query is the query builder object which allows us to build queries
        # first() gets the first row and SQLAlchemy converts it to a UserModel
        # object
        return cls.query.filter_by(id=_id).first()
