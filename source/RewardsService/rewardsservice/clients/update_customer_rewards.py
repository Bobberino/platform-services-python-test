import tornado
from tornado import httpclient


def update_customer_rewards(email_address, amount):

    http_client = httpclient.HTTPClient()

    url = "http://localhost:7050/customers/{}/{}".format(email_address, amount)
    print("url is: ", url)

    req = tornado.httpclient.HTTPRequest(url)
    try:
        response = http_client.fetch(req)
        print(response.body)
    except httpclient.HTTPError as e:
        # HTTPError is raised for non-200 responses; the response
        # can be found in e.response.
        print("Error1: " + str(e))
    except Exception as e:
        # Other errors are possible, such as IOError.
        print("Error2: " + str(e))
    http_client.close()


update_customer_rewards('customer02@gmail.com', 150)
