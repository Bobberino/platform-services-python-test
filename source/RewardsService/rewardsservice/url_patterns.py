from handlers.rewards_handler import RewardsHandler, CustomersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomersHandler),  # Endpoint 3
    (r'/customers/(?P<email_address>\w+)', CustomersHandler),  # Endpoint 2
    (r'/customers/(?P<email_address>\w+)/(?P<order_amount>\w+)', CustomersHandler),  # Endpoint 1
]
