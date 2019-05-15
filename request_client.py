#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import base64
import requests
import time
import M2Crypto
import json
from operator import itemgetter

from log import *
import config

class RequestClient(object):
    def __init__(self, api_url, acess_token, public_key, private_key, requests_params=None):
        self.API_URL = api_url
        self.ACESS_TOKEN = acess_token
        self.PUBLIC_KEY = public_key
        self.PRIVATE_KEY = private_key
        self.session = self._init_session()
        self._requests_params = requests_params

    def _init_session(self):
        session = requests.session()
        session.headers.update({'Content-Type': 'application/json',
                                'Accept': 'application/json',
                                'User-Agent': 'biger/python',
                                'BIGER-ACCESS-TOKEN': self.ACESS_TOKEN})
        return session

    def _create_api_uri(self, path):
        return self.API_URL + '/' + path

    def _sign(self, data):
        try:
            print "data:" + data
            sign_key = M2Crypto.RSA.load_key_string(self.PRIVATE_KEY)
            sha256_str = hashlib.sha256(data.encode('utf-8'))
            print "base64 sha256_str: " + base64.b64encode(sha256_str.digest())
            signature = sign_key.private_encrypt(sha256_str.digest(), M2Crypto.RSA.pkcs1_padding)
            return base64.b64encode(signature)
        except Exception as e:
            ERROR_LOG("get sign failed :%s " % (e))
            return ""

    def _verify(self, data, signature):
        verify_key = M2Crypto.RSA.load_pub_key_bio(M2Crypto.BIO.MemoryBuffer(self.PUBLIC_KEY))
        plain_signature = verify_key.public_decrypt(base64.b64decode(signature), M2Crypto.RSA.pkcs1_padding)
        print "base64 plain_signature: " + base64.b64encode(plain_signature)
        if plain_signature == hashlib.sha256(data.encode('utf-8')).digest():
            return 0
        return 1

    def _generate_signature(self, method, params, expire_ts, body = None):
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in params])
        sign_string = query_string + method + str(expire_ts)
        if body:
            sign_string += body
        return self._sign(sign_string)

    def _order_params(self, data):
        params = []
        for key, value in data.items():
                params.append((key, value))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        return params

    def _request(self, method, uri, body = None, **kwargs):
        response = None
        if self._requests_params:
            kwargs.update(self._requests_params)
        ordered_data = self._order_params(kwargs)
        expire_ts = int(time.time() + 5 ) * 1000 * 1000
        self.session.headers['BIGER-REQUEST-EXPIRY'] = str(expire_ts)
        self.session.headers['BIGER-REQUEST-HASH'] = self._generate_signature(method, ordered_data, expire_ts, body)
        if body and (method == 'POST' or method == 'PUT'):
            response = getattr(self.session, method.lower())(uri, data = body, params = ordered_data)
        else:
            response = getattr(self.session, method.lower())(uri, params = ordered_data)
        return self._handle_response(response)

    def _request_api(self, method, path, body=None, **kwargs):
        uri = self._create_api_uri(path)
        DEBUG_LOG("request url: " + uri)
        return self._request(method, uri, body, **kwargs)

    def _handle_response(self, response):
        #print self.session.headers
        if response.status_code != 200:
            ERROR_LOG("status_code wrong, detail is:%s,%s" % (response.status_code, response.text))
            return
        else:
            try:
                return response.json()
            except ValueError:
                ERROR_LOG("Invalid Response: %s" % response.text)

    def _get(self, path, **kwargs):
        return self._request_api('GET', path, None, **kwargs)

    def _post(self, path, body=None, **kwargs):
        return self._request_api('POST', path, body, **kwargs)

    def _delete(self, path, **kwargs):
        return self._request_api('DELETE', path, None, **kwargs)

    def _put(self, path, body=None, **kwargs):
        return self._request_api('PUT', path, body, **kwargs)


    """
    Biger Public Api 
    """

    # 查询钱包
    def get_accounts(self):
        return self._get("exchange/accounts/list/accounts")

    #查询指定单
    #exchange/orders/get/43960eab-d040-4eca-a4cd-bb20473e9960
    def query_order(self, orderid):
        return self._get("exchange/orders/get/" + orderid)

    #查询当前所有单
    #exchange/orders/current?symbol={ symbol }&side={ side }&offset={ offset=}&limit={ limit } 
    def query_current_all_orders(self, symbol, side, offset = 0, limit = 20):
        params = {
            "symbol"    : symbol.upper(),
            "side"      : side.upper(),
            "offset"    : str(offset),
            "limit"     : str(limit)
        }
        return self._get("exchange/orders/current", **params)

    #限价单
    #exchange/orders/create
    def put_limit_order(self, symbol, side, price, amount):
        body = {
            "symbol"    :  symbol.upper(),
            "side"      :  side.upper(),
            "price"     :  price,
            "orderQty"  :  amount,
            "orderType" :  "LIMIT"
        }
        return self._post("exchange/orders/create", json.dumps(body))

    #撤销订单
    #exchange/orders/cancel/
    def cancel_order(self, orderid):
        return self._put("exchange/orders/cancel/" + orderid)

if __name__ == '__main__':
    #私钥文件
    private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIICWgIBAAKBgFUIytlnjO9kbfSXh0D8Rkar79Nblt6sWi2SLJqMpyxlzqKrzhkW
LpEgtaCmfgUyDlxwpL38waWXRA4BHVvzRUztvH4e3gObjwZxenXpl8Au5Sc85sm6
mnyV2StjeYeWOKDyJ87/nBC8gNaMb65Z38kPmLuFESvCszmEklxRqL6xAgMBAAEC
gYA6CN4osnuFhs1keWZd+88avI3ZelDleEuzfmfisswFiRYV/5uRk4oEkoZjNj4b
3aXfgSFuaOrg0PQpeqlG8CkDJnhGEe5t4GNQQOGDI2fnQ7UXAjQSFtISJQu9I8Oz
wxRHr+B81trIyzLja+AYGrDm3/1SSBAy5+292XyaJW80gQJBAJRNPpCUtsALqcby
wUhZAU2GhdLv7tZJPTSxQLrt2vB/tw1XPC8hTOxlvg2lOBjerfyLxcYhOpT6E3lb
coq69mUCQQCSyYQWbwfQ7egcq044U+JkHWm9av6LSC0RxZj5xLqS5zwyVSXvQEu5
DbAPaiWydf5EzEtiVwoWI4bMSbYSJoxdAkBSrtpyC6f0XMxUkqX2q0ERsy3LlGAp
8v1/8k9vqQuHSP2LH5b7g+p6ZqNWwkYLf6OriVZEB+S8iMzwvW6YMHMNAkBS0T+l
KJ/QUWpUQpKvVSS2N6IhLOzQyLgk/seApG5f0/cyrrfodO5ESmS7TbhXKBt91YXy
xgj61LCJMk13kChBAkBwXwAxM5c0qPMbLs2mKDQbqb6KYgcFQZOjsj8u3T6zQvnX
4jXF5U9sgNwyC/2IYVJvMAh9hXlFtEeGS3w2XL2M
-----END RSA PRIVATE KEY-----'''
    
    private_key_pkcs8 = '''-----BEGIN PRIVATE KEY-----
MIICdAIBADANBgkqhkiG9w0BAQEFAASCAl4wggJaAgEAAoGAVQjK2WeM72Rt9JeH
QPxGRqvv01uW3qxaLZIsmoynLGXOoqvOGRYukSC1oKZ+BTIOXHCkvfzBpZdEDgEd
W/NFTO28fh7eA5uPBnF6demXwC7lJzzmybqafJXZK2N5h5Y4oPInzv+cELyA1oxv
rlnfyQ+Yu4URK8KzOYSSXFGovrECAwEAAQKBgDoI3iiye4WGzWR5Zl37zxq8jdl6
UOV4S7N+Z+KyzAWJFhX/m5GTigSShmM2Phvdpd+BIW5o6uDQ9Cl6qUbwKQMmeEYR
7m3gY1BA4YMjZ+dDtRcCNBIW0hIlC70jw7PDFEev4HzW2sjLMuNr4BgasObf/VJI
EDLn7b3ZfJolbzSBAkEAlE0+kJS2wAupxvLBSFkBTYaF0u/u1kk9NLFAuu3a8H+3
DVc8LyFM7GW+DaU4GN6t/IvFxiE6lPoTeVtyirr2ZQJBAJLJhBZvB9Dt6ByrTjhT
4mQdab1q/otILRHFmPnEupLnPDJVJe9AS7kNsA9qJbJ1/kTMS2JXChYjhsxJthIm
jF0CQFKu2nILp/RczFSSpfarQRGzLcuUYCny/X/yT2+pC4dI/YsflvuD6npmo1bC
Rgt/o6uJVkQH5LyIzPC9bpgwcw0CQFLRP6Uon9BRalRCkq9VJLY3oiEs7NDIuCT+
x4Ckbl/T9zKut+h07kRKZLtNuFcoG33VhfLGCPrUsIkyTXeQKEECQHBfADEzlzSo
8xsuzaYoNBupvopiBwVBk6OyPy7dPrNC+dfiNcXlT2yA3DIL/YhhUm8wCH2FeUW0
R4ZLfDZcvYw=
-----END PRIVATE KEY-----'''

    #公钥文件
    public_key = '''-----BEGIN PUBLIC KEY-----
MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgFUIytlnjO9kbfSXh0D8Rkar79Nb
lt6sWi2SLJqMpyxlzqKrzhkWLpEgtaCmfgUyDlxwpL38waWXRA4BHVvzRUztvH4e
3gObjwZxenXpl8Au5Sc85sm6mnyV2StjeYeWOKDyJ87/nBC8gNaMb65Z38kPmLuF
ESvCszmEklxRqL6xAgMBAAE=
-----END PUBLIC KEY-----'''

    conf = config.Config()
    LOG_INIT()
    #base_url = "https://pub-api.biger.in"
    base_url = "http://pub-api.qa.ccx123.com"
    #base_url = "http://127.0.0.1:10241"
    AcessToken = "maxiao"  
    #__init__(self, api_url, acess_token, public_key, private_key, requests_params=None):
    req = RequestClient(conf.RESP_HTTP_API_URL, conf.ACCESS_TOCKEN, conf.PUBLIC_KEY, conf.PRIVATE_KEY)
    #req = RequestClient(conf.RESP_HTTP_API_URL, conf.ACCESS_TOCKEN, public_key, private_key)
    #req.get_accounts()
    #enc_data = req._sign("GET123456789")
    #print "singed data: " + enc_data

    #print req._verify("GET123456789",enc_data)
    #dec_data = 'HQMM4FK00zEX51K1ieww2MWZwc6MmRHa+u0LqqPE1GygID89PvCl5GTWxyMf0SqEMUyijJryGl2IflVjDqri621ioHbW0zB/ev0mUwRXG+8+d+TwSoc2xH34DNqclpmwUX+yRrruahPdhjTpt1614vBvIo3qqPADjknszvJbuM0='
    #print req._verify("GET123456789",dec_data)
    print req.put_limit_order("BGUSDT", "BUY", "0.000001", "1")

    #print req.query_current_all_orders("BGUSDT", "BUY")
    #print req.query_current_all_orders("BGUSDT", "SELL")

    #print req.query_order("43960eab-d040-4eca-a4cd-bb20473e9960")

    #print req.cancel_order("43960eab-d040-4eca-a4cd-bb20473e9960")


