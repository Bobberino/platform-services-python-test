from tornado import web, escape, ioloop, httpclient, gen


def get_rewards():
    http_client = httpclient.HTTPClient()

    try:
        response = http_client.fetch("http://localhost:7050/rewards")
        print(response.body)
    except httpclient.HTTPError as e:
        # HTTPError is raised for non-200 responses; the response
        # can be found in e.response.
        print("Error: " + str(e))
    except Exception as e:
        # Other errors are possible, such as IOError.
        print("Error: " + str(e))
    http_client.close()


get_rewards()
