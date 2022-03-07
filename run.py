# this file is needed as in app.py the init_app function isn't run until
# the app is running from the terminal using python
# we call the init_app method on the db variable and pass in the app
# variable as a parameter as the app variable contains an instance of our
# flask app
# further up in app.py is db.create_all()
# when the app is run from the terminal it runs the app before running the
# line db.create_all()
# when the app is run from uwsgi using heroku it tries to run the line
# db.create_all() before running the app, which causes an error
# we can't import db at the top of app.py as that will cause a circular import
# so we need to import the app and db variables into this file
# from app.py and db.py
from app import app
from db import db

# we then call the init_app method on the db variable and pass in the app
# variable as a parameter as the app variable contains an instance of our
# flask app
db.init_app(app)

# this is a decorator that is going to affect the method below it
# it's going to run the method before the first request into this app
# without this SQLAlchemy will just create the database file without any
# tables in it
@app.before_first_request
def create_tables():
    # the create_all method is called from the SQLAlchemy object
    # this will create 'sqlite:///data.db' and all the tables in it unless
    # they exist already
    # in models.user the users table is defined
    # in models.item the items table is defined
    # in models.store the stores table is defined
    # SQLAlchemy only creates the tables that it sees because it goes through
    # imports, for example we have imported into app.py an instance of the Store
    # class from resources.store and resources.store has imported an instance
    # of the StoreModel class from models.store and in models.store the stores
    # table is defined along with the columns for that table
    # you could also import a model directly into app.py if there was no
    # resource for that model
    db.create_all()
