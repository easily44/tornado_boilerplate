from handlers.base import BaseHandler


class TestMysqlHandler(BaseHandler):
    async def get(self):
        print(1)
        await self.mysql.connect()
        print(2)
        cur = await self.mysql.conn.cursor()
        print(3)
        await cur.execute('select * from course_info')
        print(4)
        r = await cur.fetchall()
        print(r)
        await cur.close()

        self.write('test2')


class TestMysqlPoolHandler(BaseHandler):
    async def get(self):
        print(1)
        with (await self.mysql_pool) as conn:
            print(2)
            cur = await conn.cursor()
            print(3)
            await cur.execute('select * from course_info')
            print(4)
            r = await cur.fetchall()
            print(r)
            await cur.close()
        self.write('test3')


class TestMysqlSqlHandler(BaseHandler):
    async def get(self):
        course_id = self.get_argument('course_id', '')
        if not course_id:
            self.error_response(100, 'no course_id')

        asdfvf = await self.mysql.get_seq_ids(course_id)

        self.success_response({})


