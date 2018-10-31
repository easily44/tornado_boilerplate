from handlers.base import NotFoundHandler
from handlers.test import TestHandler, TestMysqlHandler, TestMysqlPoolHandler, \
    TestESHandler


url_patterns = [
    (r'/test', TestHandler),
    (r'/testmysql', TestMysqlHandler),
    (r'/testmysqlpool', TestMysqlPoolHandler),
    (r'/testes', TestESHandler),
]

url_patterns.extend([
    (r'.*', NotFoundHandler),
])
