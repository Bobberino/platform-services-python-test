import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customer = list(db.customers.find({}, {"_id": 0}))

        self.write(json.dumps(customer))

    @coroutine
    def post(self, email_address, order_value):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        #db.create_collection("customers")
        db.customers.insert({"email_address": "customer01@gmail.com", "order_amount": "100"})


