#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import glob


class Config(object):
    def __init__(self, cfg_path='cfg/bgcli.cfg'):
        # 从配置文件中获取初始化参数
        cfg = configparser.ConfigParser()
        cfg.read(glob.glob(cfg_path), encoding='utf-8')
        self.PRIVATE_KEY = cfg.get('RSA', 'private_key').decode('utf-8').encode('utf-8')
        self.PUBLIC_KEY = cfg.get('RSA', 'public_key').decode('utf-8').encode('utf-8')
        self.ACCESS_TOCKEN = cfg.get('RESP_HTTP_API', 'access_tocken').decode('utf-8').encode('utf-8')
        self.RESP_HTTP_API_URL = cfg.get('RESP_HTTP_API', 'url').decode('utf-8').encode('utf-8')
        self.WEBSOCKET_PATH = cfg.get('websocket', 'path').decode('utf-8').encode('utf-8')
        self.SYMBOL = cfg.get('websocket', 'symbol').decode('utf-8').encode('utf-8')
        self.HEARTBEAT_INTERVAL = int(cfg.get('websocket', 'heartbeat_interval'))
        self.SUBSCRIBE = cfg.get('websocket', 'subscribe').decode('utf-8').encode('utf-8')
        self.HEARTBEAT = cfg.get('websocket', 'heartbeat').decode('utf-8').encode('utf-8')
        self.PARSER = cfg.get('websocket', 'parser').decode('utf-8').encode('utf-8')
