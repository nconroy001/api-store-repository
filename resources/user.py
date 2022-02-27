# this is the User object
# it's going to be a store of data
# so now when we create a user object
# it will be the same as creating a dictionary for the user

# we're going to add the ability to retrieve user objects from the database
# we import sqlite3 so the class can interact with sqlite
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

# the UserRegister class is a resource
# it needs to be a resource so we can add it to the api using flask restful
# we could also use a flask end point instead of a resource to register users
# Flask-RESTful provides a Resource base class that can define the routing for
# one or more HTTP methods for a given URL
# The add_resource function in app.py registers the routes with the framework
# using the given endpoint
# the endpoint defined in the UserRegister class resource is post
# the API deals with resources such as users, stores and students
# the resource is used to map endpoints such as the get verb and the post verb
# to the /item or /name HTTP methods
# mapping is the process of using a map (a higher-order function) that usually
# either takes in one or more functions as arguments or returns a function
# as a result
# for example, the get verb is used to define the name of the get function
# the get function takes in name as an argument, which is passed from the
# /name HTTP method at the end of the URL
# the get function then searches the database for that name and returns
# that name from the database if it is found
# so in this case the map is a function that takes in an HTTP verb as an
# argument and returns data as a result
# methods that clients don't interact with directly don't belong in a resource
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    # we need to create the post method which will be called when we post
    # some data to the user register
    def post(self):
        data = UserRegister.parser.parse_args()

        # if the username entered already exists an error message occurs
        if UserModel.find_by_username(data['username']):
            # the return response code 400 means 'bad request'
            # if this return occurs then we'll exit from the method
            return {"message": "A user with that username already exists"}, 400

        # we initialise a variable called user and place in it
        # an instance of the UserModel class which was imported from models.user
        # at the top of this page
        # and insert the data from the parser into that UserModel instance
        # as the init function of the UserModel class in
        # models.user takes in username and password as arguments
        # **data means using each of the keys in the dictionary in the data
        # variable which contains data from the parser (username and password)
        # in dictionary format, the username in the init function argument
        # equals the username value in the data variable and the password
        # in the init function argument equals the password in the data variable
        user = UserModel(**data)
        # we then call the save_to_db function from that instance
        # of the UserModel class in the user variable
        user.save_to_db()

        # the return response code 201 means 'created'
        return {"message": "User created successfully"}, 201
