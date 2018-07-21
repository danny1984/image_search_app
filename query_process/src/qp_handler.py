# coding: utf-8

import sys, datetime
from idls.qp_idl.query_process.ttypes import *
from vector_gen.tf_vector_gen import *

class QueryProcessServiceHandler:
    def __init__(self, conf, logger):
        self._logger = logger
        self._conf   = conf
        self._vec_gen = VectorGen(conf, logger)

    def doQueryProcess(self, req):
        self._logger.debug("Get one request")
        start = datetime.datetime.now()

        # search function
        ret = self._doQueryProcess(req)

        final_end = datetime.datetime.now()
        self._logger.debug("Done search, respone time {}".format((final_end - start)))
        return ret

    def _doQueryProcess(self, req):

        # step 1. image to vector
        list_image_vectors = self._vec_gen.gen_vector(req.img_urls)
        ret_vec = QPReturnVector(list_image_vectors)
        self._logger.debug(list_image_vectors)

        listDebug = []
        ret_info = QPReturnInfo(len(list_image_vectors), len(list_image_vectors[0]), listDebug)

        srch_rslt = QPSearchResult(0, ret_info, ret_vec)
        return srch_rslt

