# coding: utf-8
import os, sys
cur_path = os.getcwd()
sys.path.append(cur_path+"/../")

from util.util import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol

from idls.sp_idl.search_plan.ttypes import *
from idls.qp_idl.query_process.ttypes import *
from idls.is_idl.image_searcher import ImageSearcherService
from idls.is_idl.image_searcher.ttypes import *

class ISHelper:

    # def __init__(self, ip, port, sp_req, qp_result):
    #     self._ip    = ip
    #     self._port  = port
    #     self._sp_req    = sp_req
    #     self._qp_result = qp_result

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
            istransport = TSocket.TSocket(self._ip, self._port)
            istransport = TTransport.TBufferedTransport(istransport)
            isprotocol = TCompactProtocol.TCompactProtocol(istransport)
            isHelper = ImageSearcherService.Client(isprotocol)
            istransport.open()

            splogger.debug("Sp access search");
            isReq = ISRequest(0, self._sp_req.comp_id, self._sp_req.craft_id,
                                self._sp_req.styles, self._qp_result.ret_vec.list_image_vectors,
                                self._qp_result.ret_info.img_dim, self._sp_req.srch_params)
            #splogger.debug(isReq)
            isRslt = isHelper.doSearch(isReq)
            splogger.debug("is return")
            splogger.debug(isRslt)

            istransport.close()

        #except Thrift.TException, ex:
        except Exception as ex:
            splogger.info( "{}".format(ex.message))
            isRetStatus = ISReturnStatus.ERROR_NO_CRAFT_ID
            isRetInfo = ISReturnInfo(0, 0, [])
            isRetProd = ISReturnProduct([])
            isRslt = ISSearchResult(isRetStatus, isRetInfo, isRetProd)

        return isRslt


# def is_test():
#     # 构造 sp 请求
#     styles   = set([1,2])
#     img_urls = []
#     img_urls.append('/Users/danny/Documents/devenv/tf_vir/workspace/imagesearch/data/test_data/IMG_3592.JPG')
#     img_urls.append('/Users/danny/Documents/devenv/tf_vir/workspace/imagesearch/data/test_data/IMG_3594.JPG')
#     params = {}
#     params['debug'] = "1"
#     sp_req = SPRequest(0, 1, 1, styles, img_urls, params)
#
#     # 构造 qp 结果
#     listDebug = []
#     ret_info = QPReturnInfo(2, 2, listDebug)
#     image_vecs  = []
#     vec_path1 = '/Users/danny/Documents/devenv/tf_vir/workspace/imagesearch/vecsearch/imgvec/output/v3_vec/imagevector/IMG_3659.JPG.txt'
#     with open(vec_path1) as fin:
#         vec_str = fin.readline()
#         imgvec = [float(x) for x in vec_str.split(",")]
#         image_vecs.append(imgvec)
#     vec_path2 = '/Users/danny/Documents/devenv/tf_vir/workspace/imagesearch/vecsearch/imgvec/output/v3_vec/imagevector/IMG_3660.JPG.txt'
#     with open(vec_path2) as fin:
#         vec_str = fin.readline()
#         imgvec = [float(x) for x in vec_str.split(",")]
#         image_vecs.append(imgvec)
#
#     ret_vec = QPReturnVector(image_vecs)
#     qp_rslt = QPSearchResult(0, ret_info, ret_vec)
#
#     isHelper = ISHelper("localhost", 4088, sp_req, qp_rslt)
#     isHelper.IS_Access()
#
#
# is_test()