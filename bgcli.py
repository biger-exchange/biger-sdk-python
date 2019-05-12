#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import socket
import getopt
import errno
import string
import signal
import threading
import os

from log import *
import config
import biger_websocket


def handle_cmd(cmd):
    if cmd != "":
        arr = cmd.split(' ')
        print len(arr)
    else:
        return "command request error!"


def wesocket_service():
    global wsc, conf
    wsc = biger_websocket.WebsockClient(conf)
    wsc.run();

def handle_request(client, address):
    try:
        result = "handle request error"
        client.settimeout(3)
        buf = client.recv(2048)
        if len(buf) > 2:
            bodylen = string.atoi(buf[0:2])
            if bodylen == len(buf):
                result = handle_cmd(buf[2:])
        client.send(result)
    except socket.timeout:
        pass
    except socket.error as (code, msg):
        if code != errno.EINTR:
            ERROR_LOG("handle request got errno(%s)", msg)
    client.close()


def signal_term(signum, frame):
    global graceful_shutdown, wsc
    WARNING_LOG("got singal term")
    graceful_shutdown = False
    if wsc.wsapp:
        wsc.wsapp.close()

def usage():
    print """
    -h --help             print the help
    -c --conf             load config, e.g python ./bgcli.py -c cfg/bgcli.cfg
    -v --version          current version  
    """

def parse_opt():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:c:v", ["help", "conf=", "version"])
    except getopt.GetoptError:
        """ print help information and exit """
        usage()
        sys.exit()
    else:
        for op, value in opts:
            if op in ("-c", "--conf"):
                global conf
                conf = config.Config(value)
                LOG_INIT(value)
            elif op in ("-v", "--version"):
                print "version 0.0.1"
            elif op in ("-h"):
                usage()
                sys.exit()


def main(ip = '', port = 8698, listen_num = 10):
    global graceful_shutdown
    parse_opt()
    signal.signal(signal.SIGINT, signal_term)
    service_router_thread = threading.Thread(name='wesocket_service', target=wesocket_service, args=())
    service_router_thread.start()
    if ip == '':
        ip = 'localhost'
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(5)
        sock.bind((ip, port))
        sock.listen(listen_num)
        NOTICE_LOG("server started, listenning on %d", port)
    except socket.error as (code, msg):
        if code != errno.EINTR:
            ERROR_LOG("cur pid[%d] set server failed! errno(%d), msg:%s", os.getpid(), code, msg)
            graceful_shutdown = False

    while graceful_shutdown:
        try:
            client, address = sock.accept()
            thread = threading.Thread(name='msvr_handlesock', target=handle_request, args=(client, address))
            thread.start()
        except socket.timeout:
            pass
        except socket.error as (code, msg):
            if code != errno.EINTR:
                ERROR_LOG("listen socket errno(%d), msg:%s", code, msg)
    sock.close()
    service_router_thread.join();


if __name__ == '__main__':
    conf = None
    wsc = None
    graceful_shutdown = True
    main()
