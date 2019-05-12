#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from log import *
import request_client
import json

class Message:
        def __init__(self):
                #私钥文件
                self.private_key = '''-----BEGIN RSA PRIVATE KEY-----
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
    
                #公钥文件
                self.public_key = '''-----BEGIN PUBLIC KEY-----
MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgFUIytlnjO9kbfSXh0D8Rkar79Nb
lt6sWi2SLJqMpyxlzqKrzhkWLpEgtaCmfgUyDlxwpL38waWXRA4BHVvzRUztvH4e
3gObjwZxenXpl8Au5Sc85sm6mnyV2StjeYeWOKDyJ87/nBC8gNaMb65Z38kPmLuF
ESvCszmEklxRqL6xAgMBAAE=
-----END PUBLIC KEY-----'''

        # 鉴权信息
        def _auth(self, access_tocken):
                pass

        def _query(self, ws, cmd, params, req_id):
                command='{"method":"%s", "params":[%s], "id": %d}'% (cmd, params, req_id)
                DEBUG_LOG("Sending " + command + " ...")
                ws.send(command)

        # 订阅
        def subscribe(self, ws, symbol):
                self._query(ws,'kline.subscribe','"%s", 900' % (symbol), 1)
                self._query(ws,'price.subscribe','"%s"' % (symbol) , 2)

        # 心跳
        def heartbeat(self, ws):
        	self._query(ws, 'server.ping', '', time.time())

        # 处理接受消息
        def service_route(self, ws, message, conf):
                DEBUG_LOG("recieved message: " + message)
                if not conf:
                        return
                req = request_client.RequestClient(conf.RESP_HTTP_API_URL, conf.ACCESS_TOCKEN, self.public_key, self.private_key)
                res = req.query_current_all_orders(conf.SYMBOL, "BUY")
                DEBUG_LOG("query current all orders: " + str(res))
