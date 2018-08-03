# coding: utf-8

import sys, datetime
# my custom utility
from idls.is_idl.image_searcher.ttypes import *
from index_helper.index_helper import *

class ImageSearcherServiceHandler:

    def __init__(self, conf, logger):
        self._conf      = conf
        self._logger    = logger
        # _vecIndex - kkv <comp, craft, index_info>
        #               index_info 结构体 见vec_index.py
        self._vecIndex  = self._index_load()

    def doSearch(self, req):
        self._logger.debug("Get one request")
        start = datetime.datetime.now()

        # search function
        ret = self._doVectorSearch(req)
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
            isRetStatus = ISReturnStatus.SEARCH_OK
            if not self._vecIndex.has_key(comp_id):
                isRetStatus = ISReturnStatus.ERROR_NO_COMP_ID
            else:
                isRetStatus = ISReturnStatus.ERROR_NO_CRAFT_ID

            isRetInfo = ISReturnInfo(0, 0, [])
            isRetProd = ISReturnProduct([])

            isRet = ISSearchResult(isRetStatus, isRetInfo, isRetProd)
            return isRet

    def _search_and_sort(self, req, index_info):
        top_k = self._conf["return_top_k"]
        query_vecs = req.query_vecs
        img_dis, img_name = index_info.doSearch(query_vecs, top_k)
        # TODO: 排序
        # prod_id = RankerBaseline(img_dis, img_name)
        isRetStatus = ISReturnStatus.SEARCH_OK
        isRetInfo = ISReturnInfo(len(img_name), len(img_name), [])
        isRetProd = ISReturnProduct(img_name)
        isRet = ISSearchResult(isRetStatus, isRetInfo, isRetProd);
        return isRet


    def _index_load(self):
        ih = IndexHelper(self._conf, self._logger)
        return ih.IndexHelper()
