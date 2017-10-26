from tornado import web, escape, ioloop, httpclient, gen
import tornado
import urllib.parse


def get_customer(emailAddress):

    http_client = httpclient.HTTPClient()

    url = "http://localhost:7050/customers/{}".format(emailAddress)
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


get_customer('customer01@gmail.com')
