# coding: utf-8
import sys, os, logging
cur_path = os.getcwd()
sys.path.append(cur_path+"/../")

islogger = logging.getLogger('image_search')
islogger.setLevel(logging.DEBUG)
# 写入到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(filename)s-%(lineno)d:    %(message)s')
ch.setFormatter(formatter)
islogger.addHandler(ch)


import yaml

conf_file_path = '../conf/is.yaml'
with open(conf_file_path) as is_conf_file:
    if is_conf_file:
        is_conf = yaml.load(is_conf_file.read())
        islogger.info("Conf:")
        #islogger.info(sp_conf["services"]["qp"])
    else:
        islogger.fatal("Load conf {} error!".format(conf_file_path))
        sys.exit(-1)
