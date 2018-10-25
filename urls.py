from handlers.base import NotFoundHandler
from handlers.test import TestHandler, TestMysqlHandler, TestMysqlPoolHandler


url_patterns = [
    (r'/test', TestHandler),
    (r'/testmysql', TestMysqlHandler),
    (r'/testmysqlpool', TestMysqlPoolHandler),
]

url_patterns.extend([
    (r'.*', NotFoundHandler),
])
