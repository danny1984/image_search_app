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
from thrift.protocol  import TBinaryProtocol
from thrift.server    import TServer

# my custom utility
from util.util import *
from is_handler import ImageSearcherServiceHandler

handler   = ImageSearcherServiceHandler(is_conf, islogger)
processor = ImageSearcherService.Processor(handler)
is_ip     = is_conf["services"]["is"]["ip"]
is_port   = is_conf["services"]["is"]["port"]
transport = TSocket.TServerSocket(is_ip, is_port)
tfactory  = TTransport.TBufferedTransportFactory()
pfactory  = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

islogger.info("=================================================================")
islogger.info("Starting Search Plan in ip \"{}\" and port {}".format(is_ip, is_port))

server.serve()

islogger.info("Done")

