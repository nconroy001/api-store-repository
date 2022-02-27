# from db.py we need to import the db variable which contains an instance
# of the SQLAlchemy object
from db import db

# the StoreModel class is going to extend db.Model
# (receive db.Model as an argument)
# and that's going to tell the SQLAlchemy entity that the StoreModel class
# is something we're going to be saving to and retrieving
# from a database, so it's going to create that mapping between the database
# and this object
class StoreModel(db.Model):
    # we need to tell SQLAlchemy that the table in the database that data from
    # this class will be stored in is the stores table
    __tablename__ = 'stores'

    # we need to tell SQLAlchemy which columns in the database this model
    # (the StoreModel class) will be using,
    # so we initialise a variable called id and place in it an
    # instance of the db variable which calls the Column method
    # the parameters of the Column method are an instance of the db variable
    # which calls the Integer method (the datatype of that column) and a
    # variable called primary_key which contains the boolean value True,
    # meaning this column is the primary key, which means it contains unique
    # values and it's going to create an index based on it so it's easy to
    # search based on id
    # the id method will be passed in to SQLAlchemy but because there's
    # no id parameter in the init function of the StoreModel class the id
    # method won't be used
    id = db.Column(db.Integer, primary_key=True)
    # the name column must contain strings of up to 80 characters
    name = db.Column(db.String(80))

    # a back reference does the opposite of
    # store = db.relationship('StoreModel') in item.models
    # a back reference allows a store to see which items are in the items table
    # with a store id equal to it's own id, so if the store is david jones and
    # it has an id column value of 2, and in the items table a fridge and a
    # table both have a store_id column value of 2 then the fridge and table
    # would be displayed in the results
    # db.relationship('ItemModel') tells SQLAlchemy this StoreModel class has a
    # relationship with the ItemModel class
    # SQLAlchemy then looks in the ItemModel class to see what the relationship
    # is and sees that the ItemModel class defines a table with stores.id as a
    # foreign key, which means that one item is related to a store, therefore
    # there could be more than one item related to the same store, so
    # SQLAlchemy knows that the store in the store variable in item.models is a
    # single store as there is only one store that each item is related to, but
    # the items variable in store.models can be contain many items so it is a
    # list of ItemModel objects
    # if we use the lazy='dynamic' parameter then whenever we access the json
    # method we're going to get an error (unless we use .all() in the json
    # method) as we have told SQLAlchemy not to create objects from the
    # database rows and self.items in the json method is now a query builder
    # that has the ability to look into the items table and apply built-in
    # SQLAlchemy queries so we can use .all() to retrieve all the items in that
    # table (as it takes the application longer to process turning all the rows
    # into objects if we don't use lazy='dynamic' but it will make the json
    # method slower if we use .all())
    items = db.relationship('ItemModel', lazy='dynamic')

    # store.py, the store model, is our internal representation
    # so it also has to contain the properties of a store as object properties
    # so it can use those properties, such as name, to interact
    # with the database
    # so for that we're going to create an init method
    # every store has a name so it will be included as an argument
    # for the init method
    def __init__(self, name):
        # the self parameter is a reference to the current instance of the class
        # and is used to access variables that belong to the class
        # these are known as properties
        # so in the current instance of the StoreModel class the data in the
        # name argument is assigned to the name property
        self.name = name

    # the json method will return a json representation of the model (store.py)
    # so any data this model retrieves from the database can be viewed by the
    # user using json
    # json is a string in dictionary format which can be read by javascript
    # we call the json method from the SQLAlchemy object
    # we pass into the json method this class, the StoreModel class, as a
    # parameter
    # the json method returns a dictionary
    # the first item in the dictionary has a key of 'name' and the value is
    # the name column of the stores table defined in this class
    # the second item in the dictionary has a key of 'items' and the value is
    # an index which contains a list comprehension that states that for every
    # object (as SQLAlchemy converts each database row into an object unless we
    # tell it not to) in the instance of the ItemModel class (which is
    # defined as 'items' in this current class) the json method is applied to
    # that object
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    # the classmethod decorator gets evaluated after the function is defined
    # the function receives the class as the first argument, which makes it
    # available for other functions in this class to use
    # the classmethod decorator is a method bound to the class and not the
    # object of the class (the find_by_name function)
    # the classmethod decorator can modify a class state that would apply
    # across all instances of the class
    # the second argument is the name of the store we're going to look for
    # the find_by_name function needs to be a class method because it's going
    # to return an object of type StoreModel as opposed to a dictionary
    # so when functions in resources.store call the find_by_name function
    # the results will be returned via the StoreModel object (this class)
    # that's why the result of this function needs to be made available to this
    # class using the classmethod decorator
    @classmethod
    def find_by_name(cls, name):
        # the below code translates to this SQL code:
        # SELECT * FROM stores WHERE name=name LIMIT 1
        # a StoreModel object will be returned
        return cls.query.filter_by(name=name).first()

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
        db.session.add(self)
        # as it's a db.session method we can add more than one object if we want
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        # as it's a db.session method we can delete more than one object if we want
        db.session.commit()
