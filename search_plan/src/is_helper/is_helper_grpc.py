# coding: utf-8
import os, sys
cur_path = os.getcwd()
sys.path.append(cur_path+"/../")
from util.util import *

import grpc
from idls.is_idl_grpc.image_searcher import rpc_image_searcher_pb2
from idls.is_idl_grpc.image_searcher import rpc_image_searcher_pb2_grpc
from idls.sp_idl.search_plan.ttypes import *
from idls.qp_idl.query_process.ttypes import *

class ISHelperGRPC:

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
        conn = grpc.insecure_channel(self._ip + ':' + str(self._port))
        is_client = rpc_image_searcher_pb2_grpc.ImageSearcherServiceStub(channel=conn)

        splogger.debug("Sp access search");
        '''
        message ISRequest{
            enum ISRequestType{
                IMAGE_SEARCH = 0;
                SEARCH_DEBUG = 1;
            }
            ISRequestType   type        = 1;
            int32		    comp_id     = 2;
            int32		    craft_id    = 3;
            repeated int32	styles      = 4;
            repeated ISQueryVector  query_vectors = 5;
            int32          vec_dim     = 6;
            map<string, string>     srch_params = 7;
        }
        '''
        isQVs  = []
        for idx, img_vec in enumerate(self._qp_result.ret_vec.list_image_vectors):
            isQV = rpc_image_searcher_pb2.ISQueryVector(id=idx, embs=img_vec)
            isQVs.append(isQV)

        isReq = rpc_image_searcher_pb2.ISRequest(type=0, comp_id=self._sp_req.comp_id, craft_id=self._sp_req.craft_id,
                          styles=list(self._sp_req.styles), query_vectors = isQVs,
                          vec_dim=self._qp_result.ret_info.img_dim, srch_params=self._sp_req.srch_params)

        #splogger.debug(isReq)
        isRslt = is_client.doSearch(isReq)
        #splogger.debug("is return")
        #splogger.debug(isRslt)

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
#     isHelper = ISHelperGRPC("localhost", 4088, sp_req, qp_rslt)
#     isHelper.IS_Access()
#
#
# is_test()