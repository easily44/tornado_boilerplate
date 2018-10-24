import json
import random
import tornado.web
from tornado.escape import json_decode
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

    def write_error(self, status_code, **kwargs):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.finish(json.dumps({
            'error_codea': status_code,
            'error_msg': self._reason,
        }))

    async def get_external(self, url, **kwargs):
        url = url_concat(url, kwargs)
        res = await self.application.client.fetch(url, request_timeout=5)

        return self.check_response(res)

    async def post_external(self, url, **kwargs):
        params = urlencode(kwargs)
        res = await self.application.client.fetch(
            url, method='POST', body=params, request_timeout=5)
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
            self.error(500, u'{} service failed'.format(self.__class__))
        else:
            if hasattr(data, 'code'):
                if data.get('code', 0) != 0:
                    self.logger.error(
                        'error_url: {}, error_msg: {}'.format(
                            res.effective_url, data['message']))
                    self.error(data['code'], data['message'])

        return data

    def error(self, code, reason):
        """
        省的每个RequestHandler都要import HTTPError
        :param code: 错误码
        :param reason: 原因
        :return:
        """
        raise HTTPError(code, reason)

    def success_response(self, data):
        data.update({
            'error_code': 0,
            'error_msg': ''
        })
        self.write(data)
