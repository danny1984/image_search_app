# coding: utf-8

"""
file  : sp_server
desc  : 
author: danny
date  : 2018-07-15 
"""

import socket
import sys

#Thrift modules
from idls.sp_idl.idl_search_plan import SearchPlanService
from idls.sp_idl.idl_search_plan.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol  import TBinaryProtocol
from thrift.server    import TServer

# my custom utility
from util.util import *
from sp_handler import SearchPlanServiceHandler

handler   = SearchPlanServiceHandler()
processor = SearchPlanService.Processor(handler)
transport = TSocket.TServerSocket("localhost", 3207)
tfactory  = TTransport.TBufferedTransportFactory()
pfactory  = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

splogger.info("Starting Search Plan for image_search_app")

server.serve()

splogger.info("Done")

