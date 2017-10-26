from handlers.rewards_handler import RewardsHandler, CustomersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomersHandler),  # Endpoint 3
    (r'/customers/([A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]+)', CustomersHandler),  # Endpoint 2
    (r'/customers/([A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]+)/([0-9]+)', CustomersHandler),# Endpoint 1 modify order amount
]
