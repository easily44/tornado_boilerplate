import tornado.ioloop
import tornado.web
import tornado.netutil
import tornado.process
from tornado.httpserver import HTTPServer
from tornado.options import options
import asyncio
import uvloop
import settings
from urls import url_patterns
from settings import TORNADO
from tornado.httpclient import AsyncHTTPClient
from logging.config import dictConfig
from utils.mysql import Mysql
from elasticsearch_async import AsyncElasticsearch
from settings import ES_SERVER


def make_app():
    return tornado.web.Application(url_patterns, **TORNADO)


class App(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient",
                                  defaults={'Connection': 'keep-alive'})
        self.client = AsyncHTTPClient()

        # # 每次connect
        # self.mysql = Mysql(**settings.DATABASE)

        # 建立pool
        self.mysql = Mysql(**settings.DATABASE)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.mysql.create_pool())

        # es
        self.es = AsyncElasticsearch(hosts=ES_SERVER)

        dictConfig(settings.LOGGING)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = App(url_patterns, **TORNADO)
    # app.listen(options.port)
    # print('server start on {}'.format(options.port))
    # tornado.ioloop.IOLoop.current().start()

    print('server start on {}'.format(options.port))
    sockets = tornado.netutil.bind_sockets(options.port)
    tornado.process.fork_processes(0)
    server = HTTPServer(app)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.current().start()
