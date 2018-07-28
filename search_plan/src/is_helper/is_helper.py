# coding: utf-8
import os, sys
cur_path = os.getcwd()
sys.path.append(cur_path+"/../")

from util.util import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from idls.is_idl.image_searcher import ImageSearcherService
from idls.is_idl.image_searcher.ttypes import *

class ISHelper:

    def __init__(self, conf, sp_req, qp_result, reInit=False):
        self._conf  = conf
        self._ip    = conf["services"]["is"]["ip"]
        self._port  = conf["services"]["is"]["port"]
        self._sp_req    = sp_req
        self._qp_result = qp_result
        self._init_ok   = True

    def IS_Access(self):
        isRslt = ISSearchResult
        try:
            transport = TSocket.TSocket(self._ip, self._port)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            isHelper = ImageSearcherService.Client(protocol)
            transport.open()

            splogger.debug("Sp access image search");
            '''
            struct ISRequest{
                1: required ISRequestType type;
                2: required i32		comp_id;
                3: required i32		craft_id;
                4: required set<i32>	styles;
                5: required list< list<double> > query_vecs;
                6: required i32     vec_dim;
                7: optional map<string, string> srch_params;
            }
            '''
            isReq = ISRequest(0, self._sp_req.comp_id, self._sp_req.craft_id,
                                self._sp_req.styles, self._qp_result.ret_vec.list_image_vectors,
                                self._qp_result.ret_info.img_dim, self._sp_req.srch_params)

            isRslt = isHelper.doSearch(isReq)
            splogger.debug("is return")
            splogger.debug(isRslt)

            transport.close()

        except Thrift.TException, ex:
            splogger.info( "{}".format(ex.message))

        return isRslt