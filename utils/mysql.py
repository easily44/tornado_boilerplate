import aiomysql


class Mysql:
    def __init__(self, host, user, password, db, port=3306, minsize=1, maxsize=10, *args, **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.minsize = minsize
        self.maxsize = maxsize
        self.conn = None
        self.pool = None

    async def create_pool(self):
        self.pool = await aiomysql.create_pool(
            minsize=self.minsize,
            maxsize=self.maxsize,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
        )

    async def connect(self):
        self.conn = await aiomysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
        )






