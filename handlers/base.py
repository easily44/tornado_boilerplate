import json
import random
import tornado.web
from tornado.escape import json_decode
from tornado.httpclient import HTTPClientError
from tornado.httputil import url_concat
from urllib.parse import urlencode
from tornado.web import HTTPError
from tornado.log import gen_log


class BaseHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.logger = gen_log
        self.mysql = self.application.mysql
        self.mysql_pool = self.application.mysql.pool

    def error_response(self, code, msg):
        self.write({
            'error_code': code,
            'error_msg': msg,
        })
        raise tornado.web.Finish

    def success_response(self, data):
        data.update({
            'error_code': 0,
            'error_msg': ''
        })
        self.write(data)
        raise tornado.web.Finish

    async def get_external(self, url, **kwargs):
        url = url_concat(url, kwargs)
        try:
            res = await self.application.client.fetch(url, request_timeout=5)
        except HTTPClientError:
            self.logger.error('>.< GET {}'.format(url))
            self.error_response(400, 'external server error')
        else:
            return self.check_response(res)

    async def post_external(self, url, **kwargs):
        params = urlencode(kwargs)
        try:
            res = await self.application.client.fetch(
                url, method='POST', body=params, request_timeout=5)
        except HTTPClientError:
            self.logger.error('POST {}'.format(url))
            self.error_response(400, 'external server error')
        else:
            return self.check_response(res)

    def check_response(self, res):
        """
        通过状态码检查下外部系统的返回值而已
        :param res:
        :return:
        """
        if res.code < 200 or res.code >= 300 or res.error:
            self.logger.error('{} {} {}'.format(res.code, res.effective_url, res.reason))
            raise HTTPError(res.code, res.reason)
        return res

    def res_to_json(self, res):
        """
        把response实际为json的转成json
        :param res:
        :return:
        """
        data = {}
        try:
            data = json_decode(res.body)
        except ValueError as e:
            self.logger.error('response not json: {}, content: {}'.format(e, res.body))
            self.error_response(500, u'{} service failed'.format(self.__class__))
        else:
            if hasattr(data, 'code'):
                if data.get('code', 0) != 0:
                    self.logger.error(
                        'error_url: {}, error_msg: {}'.format(
                            res.effective_url, data['message']))
                    self.error_response(data['code'], data['message'])

        return data

    @property
    def es(self):
        return self.application.es


class NotFoundHandler(BaseHandler):
    """
    no handler return here
    """
    def get(self):
        self.error_response(100, u'NotHandler')



