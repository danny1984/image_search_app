# coding: utf-8
import logging

splogger = logging.getLogger('image_search_app')
splogger.setLevel(logging.DEBUG)
# 写入到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(filename)s-%(lineno)d:    %(message)s')
ch.setFormatter(formatter)
splogger.addHandler(ch)

import datetime