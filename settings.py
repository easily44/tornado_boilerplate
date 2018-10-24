import base64
import uuid

from tornado.options import define, options
# 下面导入外部配置，勿删
from conf.logging import *


define('port', default=61100, type=int)
define('debug', default=False, type=bool)


options.parse_command_line()


TORNADO = {
    'cookie_secret': base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
    'debug': options.debug,
    'gzip': True,
}

