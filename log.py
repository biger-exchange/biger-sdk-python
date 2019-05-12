#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import logging.config

global_log_var_=None
global_log_wf_var_=None

def LOG_INIT(cfg_path='cfg/bgcli.cfg'):
    global global_log_var_, global_log_wf_var_
    logging.config.fileConfig(cfg_path)
    global_log_var_ = logging.getLogger("infoLog")
    global_log_wf_var_ = logging.getLogger("warnLog")

def FATAL_LOG(*args):
    global global_log_wf_var_
    if not global_log_wf_var_:
        return False
    global_log_wf_var_.fatal(args)
    return True

def ERROR_LOG(*args):
    global global_log_wf_var_
    if not global_log_wf_var_:
        return False
    global_log_wf_var_.error(args)
    return True

def WARNING_LOG(*args):
    global global_log_wf_var_
    if not global_log_wf_var_:
        return False
    global_log_wf_var_.warning(args)
    return True

def DEBUG_LOG(*args):
    global global_log_var_
    if not global_log_var_:
        return False
    global_log_var_.debug(args)
    return True

def NOTICE_LOG(*args):
    global global_log_var_
    if not global_log_var_:
        return False
    global_log_var_.info(args)
    return True

def LOG_DESTROY():
    global global_log_var_
    global global_log_wf_var_
    global_log_var_    = None
    global_log_wf_var_ = None