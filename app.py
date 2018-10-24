import tornado.ioloop
import tornado.web
from tornado.options import options
import asyncio
import uvloop
import settings
from urls import url_patterns
from settings import TORNADO
from tornado.httpclient import AsyncHTTPClient
from logging.config import dictConfig


def make_app():
    return tornado.web.Application(url_patterns, **TORNADO)


class App(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        AsyncHTTPClient.configure(None, defaults={'Connection': 'keep-alive'})
        self.client = AsyncHTTPClient()

        dictConfig(settings.LOGGING)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = App(url_patterns, **TORNADO)
    app.listen(options.port)
    print('server start on {}'.format(options.port))
    tornado.ioloop.IOLoop.current().start()
