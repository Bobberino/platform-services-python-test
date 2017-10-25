import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from bson import json_util


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))


class CustomersHandler(tornado.web.RequestHandler):

    def get(self, emailAddress=None):
        print("in Custom Handler Get - emailAddress is: ", emailAddress)
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # Put email url back in and run with email address
        if emailAddress is None:
            print("in Custome Handler Get - emailAddress sb None, is: ", emailAddress)
            customer = list(db.customers.find({}, {"_id": 0}))
            self.write(json.dumps(customer))
        else:
            print("in Custom Handler Get - emailAddress sb emailAddress, is: ", emailAddress)
            customer_dict = db.customers.find_one({"emailAddress": "customer01@gmail.com"})
            # Handle not found
            print('customer_dict is: ', customer_dict)

            self.write(json.dumps(customer_dict, default=json_util.default))  # send back the whole record



    @coroutine
    def post(self, emailAddress, order_value):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        # calculate new rewards
        db.customers.insert({"emailAddress": "customer01@gmail.com", "order_amount": "100"})

