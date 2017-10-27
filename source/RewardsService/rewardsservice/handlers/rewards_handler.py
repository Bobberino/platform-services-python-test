import json
import tornado.web
import pymongo
from pymongo import MongoClient
from tornado.gen import coroutine
from bson import json_util


# add asynch request handlers

class RewardsHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))


class CustomersHandler(tornado.web.RequestHandler):
    def get(self, email_address=None, order_amount=None):

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # Figure out if the request if to get all customers, one specific customer
        # or to insert/update a new/existing customer.
        print("in Custom Handler Get - email_address is: ", email_address)

        if email_address is None:
            # Endpoint 3 - get all customers rewards info
            customer = list(db.customers.find({}, {"_id": 0}))
            self.write(json.dumps(customer))  # handle none -
        else:
            if order_amount is None:
                # Endpoint 2 - get a specific customers rewards information
                customer_dict = db.customers.find_one({"emailAddress": email_address})
                # Handle not found
                print('customer_dict is: ', customer_dict)

                self.write(json.dumps(customer_dict, default=json_util.default))  # send back the whole record
            else:
                # Endpoint 3 - update existing user/ add ne user

                cscr = CalculateStoreCustomerRewards()
                current_values = cscr.get_current_values(email_address)

                if current_values is None:
                    cscr.add_new_customer(email_address, order_amount)
                else:
                    cscr.update_customer(email_address, order_amount, current_values)


class CalculateStoreCustomerRewards:
    """ ** Endpoint 1: **
        # Accept a customer's order data: **email adress**
        #      (ex. "customer01@gmail.com") and **order total** (ex. 100.80).
        # Calculate and store the following customer rewards data into MongoDB. For each dollar a customer spends,
        # the customer will earn 1 reward point. For example, a customer whose order total is $100.80 earns 100
        # points and belongs to Rewards Tier A.
        # Note: a customer can only belong to one rewards tier. For example, a customer with 205 reward points belongs
        # to Rewards Tier B and cannot use the reward from Tier A. Once a customer has reached the top rewards tier,
        # there are no additional rewards the customer can earn.
            # ** Email Address: ** the customer's email address (ex. "customer01@gmail.com")
            # ** Reward Points: ** the customer's rewards points (ex. 100)
            # ** Rewards Tier: ** the rewards tier the customer has reached (ex. "A")
            # ** Reward Tier Name: ** the name of the rewards tier(ex. "5% off purchase")
            # ** Next Rewards Tier: ** the next rewards tier the customer can reach(ex. "B")
            # ** Next Rewards Tier Name: ** the name of next rewards tier(ex. "10% off purchase")
            # ** Next Rewards Tier Progress: ** the percentage the customer is away from reaching
                    the next rewards tier(ex. 0.5)
    """

    def get_current_values(self, email_address):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        customer_dict = db.customers.find_one({"emailAddress": email_address})

        return customer_dict

    def update_customer(self, email_address, order_amount, current_customer_values):

        # use existing record - current_customer_values
        print('\nIn update_customer current_customer_values are: ', current_customer_values)

        # Create new record to update
        update_record = {'emailAddress': email_address}
        # needs the database id
        update_record['_id'] = current_customer_values['_id']
        new_points = int(int(current_customer_values["rewardPoints"]) + int(order_amount))
        print('new_points is: ', new_points)
        update_record['rewardPoints'] = new_points

        print('update_record is: ', update_record)

        self.update_database(update_record)


    def add_new_customer(self, email_address, order_amount):

        print("\n\nin add_new_customer\n\n")

        # Create new record
        update_record = {}
        reward_points = int(order_amount)  # floor??? truncate?
        update_record['emailAddress'] = email_address
        update_record['rewardPoints'] = reward_points

        self.update_database(update_record)


    def update_database(self, update_record):

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        # Get the first record below - the tier the customer belongs to and
        # the next record after - the next tier.

        current_tier = db.rewards.find({"points": {"$lt": update_record['rewardPoints']}}) \
            .sort([("points", pymongo.DESCENDING)]).limit(1)

        ct1 = None
        for ct in current_tier:
            ct1 = ct

        next_tier = db.rewards.find(
            {"points": {"$gt": update_record['rewardPoints']}}
        ).sort([("points", pymongo.ASCENDING)]).limit(1)

        nt1 = None
        for nt in next_tier:
            nt1 = nt

        if ct1 is None:  # Hasn't earned rewards
            update_record['rewardsTier'] = None
            update_record['rewardsTierName'] = None
            update_record['nextRewardsTier'] = nt1['tier']
            update_record['nextRewardsTierName'] = nt1['rewardName']
            update_record['nextRewardsTierProgress'] = update_record['rewardPoints'] / int(nt1['points'])
        elif nt1 is None:  # Maxed out on rewards
            update_record['rewardsTier'] = ct1['tier']
            update_record['rewardsTierName'] = ct1['rewardName']
            update_record['nextRewardsTier'] = None
            update_record['nextRewardsTierName'] = None
            update_record['nextRewardsTierProgress'] = None
        else:
            diff = int(nt1['points']) - int(ct1['points'])
            print('diff is: ', diff)
            update_record['rewardsTier'] = ct1['tier']
            update_record['rewardsTierName'] = ct1['rewardName']
            update_record['nextRewardsTier'] = nt1['tier']
            update_record['nextRewardsTierName'] = nt1['rewardName']
            update_record['nextRewardsTierProgress'] = \
                round(1.0 - ((int(nt1['points']) - update_record['rewardPoints']) / diff), 2)

        print('update_record is: ', update_record)
        # write update record to the database - I think I need the _id as well.

        db.customers.save(update_record)
