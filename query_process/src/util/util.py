# coding: utf-8
import logging
import sys

qplogger = logging.getLogger('query_process')
qplogger.setLevel(logging.DEBUG)
# 写入到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(filename)s-%(lineno)d:    %(message)s')
ch.setFormatter(formatter)
qplogger.addHandler(ch)

import datetime

import yaml

conf_file_path = '../conf/qp.yaml'
with open(conf_file_path) as qp_conf_file:
    if qp_conf_file:
        qp_conf = yaml.load(qp_conf_file)
        qplogger.info("Conf:")
        #qplogger.info(qp_conf["services"]["qp"])
    else:
        qplogger.fatal("Load conf {} error!".format(conf_file_path))
        sys.exit(-1)
