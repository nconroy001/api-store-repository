# safe_str_cmp returns true if the strings are the same
# as some python versions don't allow ==
from werkzeug.security import safe_str_cmp
# we can import the UserModel class from the user file
# in the models folder
from models.user import UserModel

# we can use the authenticate and identity functions to log in
# users and identify them

# this function will find the user
# it calls the find_by_username method in the UserModel object
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # if the user is found and the password matches return the user
    if user and safe_str_cmp(user.password, password):
        return user

# the identity function is unique to flask jwt
# it takes in a payload which is the contents of the jwt token
def identity(payload):
    # we will extract the user id from the payload
    user_id = payload['identity']
    # once we have the user id we can retrieve the specific user
    # that matches this payload
    # by calling the find_by_id method in the UserModel object
    return UserModel.find_by_id(user_id)
