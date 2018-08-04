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
from idls.sp_idl.search_plan import SearchPlanService
from idls.sp_idl.search_plan.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol
from thrift.server    import TServer

# my custom utility
from util.util import *
from sp_handler import SearchPlanServiceHandler

handler   = SearchPlanServiceHandler()
processor = SearchPlanService.Processor(handler)
sp_ip     = sp_conf["services"]["sp"]["ip"]
sp_port   = sp_conf["services"]["sp"]["port"]
transport = TSocket.TServerSocket(sp_ip, sp_port)
tfactory  = TTransport.TBufferedTransportFactory()
pfactory  = TCompactProtocol.TCompactProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

splogger.info("Starting Search Plan in ip \"{}\" and port {}".format(sp_ip, sp_port))

server.serve()

splogger.info("Done")

