from handlers.base import NotFoundHandler
from handlers.test import TestHandler, TestESHandler
from handlers.mysqlapi import TestMysqlHandler, TestMysqlPoolHandler,\
    TestMysqlSqlHandler


url_patterns = [
    (r'/test', TestHandler),

    # es
    (r'/testes', TestESHandler),

    # mysql
    (r'/testmysql', TestMysqlHandler),
    (r'/testmysqlpool', TestMysqlPoolHandler),
    (r'/testmysqlsql', TestMysqlSqlHandler),

]

url_patterns.extend([
    (r'.*', NotFoundHandler),
])
