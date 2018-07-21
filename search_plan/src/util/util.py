# coding: utf-8

import sys, os, logging
cur_path = os.getcwd()
sys.path.append(cur_path+"/../")

splogger = logging.getLogger('search_plan')
splogger.setLevel(logging.DEBUG)
# 写入到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(filename)s-%(lineno)d:    %(message)s')
ch.setFormatter(formatter)
splogger.addHandler(ch)

import datetime

import yaml

conf_file_path = '../conf/sp.yaml'
with open(conf_file_path) as sp_conf_file:
    if sp_conf_file:
        sp_conf = yaml.load(sp_conf_file.read())
        splogger.info("Conf:")
        #splogger.info(sp_conf["services"]["qp"])
    else:
        splogger.fatal("Load conf {} error!".format(conf_file_path))
        sys.exit(-1)
