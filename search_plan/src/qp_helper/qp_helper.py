# coding: utf-8
import os, sys
cur_path = os.getcwd()
sys.path.append(cur_path+"/../")

from util.util import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from idls.qp_idl.query_process import QueryProcessService
from idls.qp_idl.query_process.ttypes import *


class QPHelper:
    def __init__(self, conf, req, reInit=False):
        self._ip     = conf["services"]["qp"]["ip"]
        self._port   = conf["services"]["qp"]["port"]
        self._sp_req = req
        self._init_ok = True

    def QP_Access(self):
        qpRslt = QPSearchResult
        try:
            transport = TSocket.TSocket(self._ip, self._port)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            qpClient = QueryProcessService.Client(protocol)
            transport.open()

            splogger.debug("Sp access qp");
            qpReq = QPRequest(0, self._sp_req.img_urls, self._sp_req.srch_params)

            qpRslt = qpClient.doQueryProcess(qpReq)
            splogger.debug("qp return")
            splogger.debug(qpRslt)

            transport.close()

        except Thrift.TException, ex:
            splogger.info( "{}".format(ex.message))

        return qpRslt