#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import glob

class Config(object):
    def __init__(self, cfg_path='cfg/bgcli.cfg'):
        # 从配置文件中获取初始化参数
        cfg = configparser.ConfigParser()
        cfg.read(glob.glob(cfg_path), encoding='utf-8')
        self.PRIVATE_KEY = cfg.get('RSA', 'private_key').decode('utf-8')
        self.PUBLIC_KEY = cfg.get('RSA', 'public_key').decode('utf-8')
        self.ACCESS_TOCKEN = cfg.get('RESP_HTTP_API', 'access_tocken')
        self.RESP_HTTP_API_URL = cfg.get('RESP_HTTP_API', 'url')
        self.WEBSOCKET_PATH = cfg.get('websocket', 'path')
        self.SYMBOL = cfg.get('websocket', 'symbol')
