# coding: utf-8

"""
file  : is_server_test_config
desc  : 
author: danny
date  : 2018-08-26 
"""

import sys, datetime
from index_helper.index_helper import *
from util.util import *

def check_config():
   ih = IndexHelper(is_conf, islogger)
   return ih.IndexHelper(True)


if __name__ == '__main__':
   check_config()
