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

    async def fetchall(self, sql):
        with (await self.pool) as conn:
            cur = await conn.cursor()
            await cur.execute(sql)
            r = await cur.fetchall()
            # print(r)
            await cur.close()
        return r

    async def fetchone(self, sql):
        with (await self.pool) as conn:
            cur = await conn.cursor()
            await cur.execute(sql)
            r = await cur.fetchone()
            # print(r)
            await cur.close()
        return r

    async def get_seq_ids(self, course_id):
        r = await self.fetchall("""
            select distinct xxx, order_id
            from gddsff 
            where course_id="{}" 
            order by order_id
        """.format(course_id))
        if r:
            return r
        else:
            return ()

    async def get_seq_top(self, course_id):
        r = await self.fetchone("""
            select distinct sdfv, order_id
            from dbfd 
            where course_id="{}" 
            order by order_id
            limit 1
        """.format(course_id))

        if r:
            return r
        else:
            return None



