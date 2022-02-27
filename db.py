# we import the SQLAlchemy object
from flask_sqlalchemy import SQLAlchemy

# we initialise a variable and place an instance of the SQLAlchemy object
# in it
# the SQLAlchemy object will link to our flask app and look at all the objects
# that we tell it to and then it's going to allow us to map those objects to
# rows in a database
# for example, when we create an ItemModel object, like the class in item.py,
# that has a column (property) called name and a column (property) called price,
# it's going to allow us to very easily put that object into our database by
# saving the object's properties into the database
db = SQLAlchemy()
