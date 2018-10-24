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


class Test2(BaseHandler):
    def get(self):
        self.write('test2')


