import tornado.httpclient
from tornado import gen
import tornado.options

@tornado.gen.coroutine
def json_fetch(http_client):
    response = yield http_client.fetch("http://localhost:7050/customers", method="GET", body=None)
    raise gen.Return(response)

@tornado.gen.coroutine
def request():
    body = {}
    http_client = tornado.httpclient.AsyncHTTPClient()
    http_response = yield json_fetch(http_client)
    print(http_response.body)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    tornado.ioloop.IOLoop.instance().run_sync(request)