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
from idls.qp_idl.query_process import QueryProcessService
from idls.qp_idl.query_process.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol  import TBinaryProtocol
from thrift.server    import TServer

# my custom utility
from util.util import *
from qp_handler import QueryProcessServiceHandler

handler   = QueryProcessServiceHandler(qp_conf, qplogger)
processor = QueryProcessService.Processor(handler)
qp_ip     = qp_conf["services"]["qp"]["ip"]
qp_port   = qp_conf["services"]["qp"]["port"]
transport = TSocket.TServerSocket(qp_ip, qp_port)
tfactory  = TTransport.TBufferedTransportFactory()
pfactory  = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

qplogger.info("Starting Query Process in ip \"{}\" and port {}".format(qp_ip, qp_port))

server.serve()

qplogger.info("Done")
