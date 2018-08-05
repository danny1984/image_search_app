# coding: utf-8
import sys, datetime
from idls.is_idl_grpc.image_searcher import rpc_image_searcher_pb2
from idls.is_idl_grpc.image_searcher import rpc_image_searcher_pb2_grpc

from util.util import *
from index_helper.index_helper import *

class ImageSearcherServiceGRPCHandler(rpc_image_searcher_pb2_grpc.ImageSearcherServiceServicer):
    def __init__(self, conf, logger):
        self._conf      = conf
        self._logger    = logger
        # _vecIndex - kkv <comp, craft, index_info>
        #               index_info 结构体 见vec_index.py
        self._vecIndex  = self._index_load()

    def doSearch(self, request, context):
        self._logger.debug("Get one request")
        start = datetime.datetime.now()

        # search function
        ret = self._doVectorSearch(request)
        self._logger.debug(ret)

        final_end = datetime.datetime.now()
        self._logger.debug("Done search, respone time {}".format((final_end - start)))
        return ret

    def _doVectorSearch(self, req):
        comp_id = req.comp_id
        craft_id = req.craft_id
        #query_vecs = req.query_vecs
        self._logger.debug("Query company {} and craft {}".format(comp_id, craft_id))

        # step 1: 找到comp和craft的 index_info
        if self._vecIndex.has_key(comp_id) and self._vecIndex[comp_id].has_key(craft_id):
            self._logger.debug("Index exists ....")
            cur_index_info = self._vecIndex[comp_id][craft_id]
            # step 2: 排序
            return self._search_and_sort(req, cur_index_info)
        else:
            self._logger.debug("Index not exists ....")
            return rpc_image_searcher_pb2.ISSearchResult(ret_status=1,
                                ret_info=rpc_image_searcher_pb2.ISReturnInfo(srch_img_cnt=0, srch_sample_cnt=0, debug_info=""),
                                ret_prod=[])

    def _search_and_sort(self, req, index_info):
        top_k = self._conf["return_top_k"]
        # TODO: 转换成数组
        '''
        message ISQueryVector{
            int32 id   = 1;
            repeated float embs  = 2;
        }
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
        query_vecs = []
        for isQV in req.query_vectors:
            query_vecs.append(isQV.embs)
        img_dises, img_names = index_info.doSearch(query_vecs, top_k)
        # TODO: 排序
        # prod_id = RankerBaseline(img_dises, img_names)
        '''
        message ISReturnInfo{
            int32	       srch_img_cnt     = 1;
            int32	       srch_sample_cnt  = 2;
            repeated string        debug_info       = 3;
        }
        
        // product list for one query
        message ISProduct {
            repeated string prod_ids  = 1;
        }
        
        message ISSearchResult{
            enum ISReturnStatus{
                SEARCH_OK = 0;
                ERROR_NO_COMP_ID = 1;
                ERROR_NO_CRAFT_ID = 2;
            }
            ISReturnStatus  ret_status  = 1;
            ISReturnInfo	ret_info    = 2;
            repeated ISProduct ret_prod    = 3;
        }
        '''
        img_cnt = 0
        ret_prods = []
        for img_name in img_names:
            isProds = rpc_image_searcher_pb2.ISProduct(prod_ids=img_name)
            ret_prods.append(isProds)
            img_cnt += len(img_name)
        retInfo = rpc_image_searcher_pb2.ISReturnInfo(srch_img_cnt=img_cnt, srch_sample_cnt=img_cnt, debug_info=[])

        return rpc_image_searcher_pb2.ISSearchResult(ret_status=0,ret_info=retInfo, ret_prod=ret_prods)

    def _index_load(self):
        ih = IndexHelper(self._conf, self._logger)
        return ih.IndexHelper()
