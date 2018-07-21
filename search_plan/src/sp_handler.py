# coding: utf-8

import sys
# my custom utility
from util.util import *
from qp_helper.qp_helper import *
from idls.sp_idl.search_plan.ttypes import *
from idls.qp_idl.query_process.ttypes import *

class SearchPlanServiceHandler:

    def doImageSearch(self, req):
        splogger.debug("Get one request")
        start = datetime.datetime.now()

        self._debugInfo(req)

        # search function
        ret = self._doImageSearch(req)
        splogger.debug(ret)

        final_end = datetime.datetime.now()
        splogger.debug("Done search, respone time {}".format((final_end - start)))

        return ret

    def _doImageSearch(self, req):
        retInfo = SPReturnInfo(0, 0, [])
        retProd = SPReturnProduct([])
        srch_rslt = SPSearchResult(0, retInfo, retProd)

        # step 1. query_process
        qp_helper = QPHelper(sp_conf, req, True)
        qpRslt = qp_helper.QP_Access()
        splogger.debug("==== Step 1. QP Return ====")
        splogger.debug(qpRslt)
        splogger.debug("===========================")

        # step 2. vector_search

        # step 3.

        '''
        enum ReturnStatus{
            SEARCH_OK,
            ERROR_1
        }
        
        struct ReturnInfo{
            1: required i32	       srch_img_cnt;
            2: required i32	       srch_sample_cnt;
            3: optional list<string> debug_info;
        }
        
        struct ReturnProduct{
            1: required list<i32> list_prods; 
        }
        
        struct SearchResult{
            1: required ReturnStatus  ret_status;
            2: required ReturnInfo	  ret_info;	
            3: required ReturnProduct ret_prod;
        }
        '''

        return srch_rslt

    def _debugInfo(self, req):
        splogger.debug(req)