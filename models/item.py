# from db.py we need to import the db variable which contains an instance
# of the SQLAlchemy object
from db import db

# both the UserModel class and the ItemModel class are going to extend db.Model
# (receive db.Model as an argument)
# and that's going to tell the SQLAlchemy entity that the ItemModel class and
# the UserModel class are things we're going to be saving to and retrieving
# from a database, so it's going to create that mapping between the database
# and these objects
class ItemModel(db.Model):
    # we need to tell SQLAlchemy that the table in the database that data from
    # this class will be stored in is the items table
    __tablename__ = 'items'

    # we need to tell SQLAlchemy which columns in the database this model
    # (the ItemModel class) will be using,
    # so we initialise a variable called id and place in it an
    # instance of the db variable which calls the Column method
    # the parameters of the Column method are an instance of the db variable
    # which calls the Integer method (the datatype of that column) and a
    # variable called primary_key which contains the boolean value True,
    # meaning this column is the primary key, which means it contains unique
    # values and it's going to create an index based on it so it's easy to
    # search based on id
    # the id method will be passed in to SQLAlchemy but because there's
    # no id parameter in the init function of the ItemModel class the id
    # method won't be used
    id = db.Column(db.Integer, primary_key=True)
    # the name column must contain strings of up to 80 characters
    name = db.Column(db.String(80))
    # the price column must contain floating point (decimal) numbers
    # with up to 2 decimal places
    price = db.Column(db.Float(precision=2))
    # the store_id column is going to be an integer because it has to match
    # exactly the store's id type as the id column in the store is an integer
    # and the foreign key is stores, which is the table name of the store
    # specified in the StoreModel class in models.store, with .id
    # as that is the column name in the stores table where the id is

    # A primary key is a column or a set of columns in a table whose values
    # uniquely identify a row in the table. A foreign key is a column or a
    # set of columns in a table whose values correspond to the values of the
    # primary key in another table.

    # the relational database engine such as sqlite won't allow us to delete a
    # table if the primary key is used as a foreign key in another table
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # we don't have to use joining (the process of taking data from multiple
    # tables and putting it into one generated view) to connect the items table
    # (defined in the ItemModel class in item.models) to the stores table
    # (defined in the StoreModel class in store.models) as SQLAlchemy does that
    # for us using the relationship method, which, when called within the
    # ItemModel class, selects any columns in the stores table that have a
    # primary key value matching the foreign key value in the items table
    # defined as stores.id, meaning the foreign key value from the items table
    # is the same as the primary key value from the stores table, so now every
    # instance of the ItemModel class has a property called store that contains
    # any rows from the stores table with an id column value that matches a
    # store_id column value in the items table, so if one of the items is a
    # fridge it might be in the myer store or the david jones store
    store = db.relationship('StoreModel')

    # item.py, the item model, is our internal representation
    # so it also has to contain the properties of an item as object properties
    # so it can use those properties, such as name and price, to interact
    # with the database
    # so for that we're going to create an init method
    # every item has a name and a price so they will be included as arguments
    # for the init method
    def __init__(self, name, price, store_id):
        # the self parameter is a reference to the current instance of the class
        # and is used to access variables that belong to the class
        # these are known as properties
        # so in the current instance of the ItemModel class the data in the
        # name and price arguments is assigned to the name and price properties
        # the store_id column in the items table is created above and whenever
        # an item is add to the table a store id needs to be assigned to it by
        # the user
        self.name = name
        self.price = price
        self.store_id = store_id

    # the json method will return a json representation of the model (item.py)
    # so any data this model retrieves from the database can be viewed by the
    # user using json
    # json is a string in dictionary format which can be read by javascript
    # jsonify takes in a python dictionary and converts it to json
    def json(self):
        return {'name': self.name, 'price': self.price}

    # the classmethod decorator gets evaluated after the function is defined
    # the function receives the class as the first argument, which makes it
    # available for other functions in this class to use
    # the classmethod decorator is a method bound to the class and not the
    # object of the class (the function)
    # the classmethod decorator can modify a class state that would apply
    # across all instances of the class
    # the second argument is the name of the item we're going to look for
    # the find_by_name function needs to be a class method because it's going
    # to return an object of type ItemModel as opposed to a dictionary
    # so when functions in resources.item call the find_by_name function
    # the results will be returned via the ItemModel object (this class)
    # that's why the result of this function needs to be made available to this
    # class using the classmethod decorator
    @classmethod
    def find_by_name(cls, name):
        # the below code translates to this SQL code:
        # SELECT * FROM items WHERE name=name LIMIT 1
        # an ItemModel object will be returned
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
        # as it's a db.session we can add more than one object if we want
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        # as it's a db.session we can delete more than one object if we want
        db.session.commit()
