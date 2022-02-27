from flask_restful import Resource
from models.store import StoreModel

# the Store class extends the Resource class which was imported from
# flask_restful
class Store(Resource):
# a store only has a name so we only need to create the get, post and delete
# end points, we don't need the put end point as that would change the store
# name
    def get(self, name):
        # this returns a specific store
        # we call the find_by_name method from the StoreModel object (which was
        # imported from models.store) and pass in the name variable as a
        # parameter
        # the result returned by the find_by_name method is placed into the
        # store variable
        # the find_by_name method may return a store object (including it's
        # items) or 'None'
        store = StoreModel.find_by_name(name)
        if store:
            # if a store object is returned by the find_by_name method then
            # the json method from the StoreModel object is called and the
            # result is returned
            return store.json()
        # if the store isn't found a tuple is returned containing a dictionary
        # and the 404 status code, which means 'Not found'
        # flask and flask sqlalchemy know to return the message in the body and
        # the code in the status code
        # if we don't enter a code to return then the code 200 is returned,
        # which means the request was successful
        return {'message': 'Store not found'}, 404

    def post(self, name):
        # if the store exists then we don't need to create a new store
        # a message is returned with the status code 400, meaning 'Bad request'
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        # if the store doesn't exist we create it by passing the name variable
        # (which was passed into the post method as a parameter)
        # into an instance of the StoreModel object and passing that instance
        # into a store variable
        store = StoreModel(name)
        # we then try to save that new store to the database by calling the
        # save_to_db method from the instance of the StoreModel object in the
        # store variable
        try:
            store.save_to_db()
        # if the new store can't be saved to the database a message is returned
        # and the status code 500 is also returned, which means there was an
        # internal server error
        except:
            return {'message': 'An error occured while creating the store'}, 500

        # if the except code didn't run then the store object is returned after
        # the json method within it is called
        # the status code 201 is also returned, which means a resource has been
        # created
        return store.json(), 201

    def delete(self, name):
        # the delete method looks to see if the store exists
        store = StoreModel.find_by_name(name)
        # if the store exists it is deleted
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        # a dictionary of store objects is returned and each store has the json
        # method called from within them
        # this is the same as in resources.item
        return {'stores': [store.json() for store in StoreModel.query.all()]}
