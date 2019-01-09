from handlers.base import BaseHandler
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import time


class AAA:
    def __init__(self):
        self.executor = ThreadPoolExecutor()

    @run_on_executor
    def aaa(self):
        time.sleep(1)


class TestHandler(BaseHandler):
    async def get(self):
        print('get')
        # res = await self.get_external('http://www.baidu.com')
        # print('end-baidu')
        a = AAA()
        await a.aaa()
        print('end')
        self.write("Hello, world!")


class TestESHandler(BaseHandler):
    """
    ES实现
    """
    async def get(self):
        t = self.get_argument('t', 1)
        # es = AsyncES()
        print('start')
        info = await self.es.info()
        print('end info')
        # g = await self.es.search(index='ecommerce', doc_type='products')
        # print('end')
        self.success_response({'data': len(info)})



