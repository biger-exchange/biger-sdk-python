#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from log import *
import request_client

class Message:
        def __init__(self):
            pass

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

        def ping(self, ws):
                DEBUG_LOG("Sending Ping ...")
                if ws.sock:
                    if not ws.sock.ping():
                        ws.sock.close()

        # 处理接受消息
        def service_route(self, ws, message, conf):
                DEBUG_LOG("Recieved message: " + message)
                if not conf:
                        return
                req = request_client.RequestClient(conf.RESP_HTTP_API_URL, conf.ACCESS_TOCKEN, conf.PUBLIC_KEY, conf.PRIVATE_KEY)
                res = req.query_current_all_orders(conf.SYMBOL, "BUY")
                DEBUG_LOG("query current all orders: " + str(res))
