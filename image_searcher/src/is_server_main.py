# coding: utf-8

"""
file  : is_server
desc  : 
author: danny
date  : 2018-07-22 
"""

import socket
import sys

#Thrift modules
from idls.is_idl.image_searcher         import ImageSearcherService
from idls.is_idl.image_searcher.ttypes  import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol  import TCompactProtocol
from thrift.server    import TServer

# my custom utility
from util.util import *
from is_handler import ImageSearcherServiceHandler

ishandler   = ImageSearcherServiceHandler(is_conf, islogger)
isprocessor = ImageSearcherService.Processor(ishandler)
is_ip     = is_conf["services"]["is"]["ip"]
is_port   = is_conf["services"]["is"]["port"]
istransport = TSocket.TServerSocket(is_ip, is_port)
istfactory  = TTransport.TBufferedTransportFactory()
ispfactory  = TCompactProtocol.TCompactProtocolFactory()

is_server = TServer.TSimpleServer(isprocessor, istransport, istfactory, ispfactory)

islogger.info("=================================================================")
islogger.info("Starting Search Plan in ip \"{}\" and port {}".format(is_ip, is_port))

is_server.serve()

islogger.info("Done")

