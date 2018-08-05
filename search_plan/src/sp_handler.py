# coding: utf-8

import sys
# my custom utility
from util.util import *
from qp_helper.qp_helper import *
from is_helper.is_helper import *
from idls.sp_idl.search_plan.ttypes import *
from idls.qp_idl.query_process.ttypes import *
from idls.is_idl.image_searcher.ttypes import *

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

        # step 1. query_process
        splogger.debug("==== Step 1. QP Access         ====")
        qp_helper = QPHelper(sp_conf, req, True)
        qpRslt = qp_helper.QP_Access()
        #splogger.debug(qpRslt)
        splogger.debug("==== Step 1. QP Access Success ====")

        # step 2. vector_search
        splogger.debug("==== Step 2. IS Access         ====")
        is_helper = ISHelper(sp_conf, req, qpRslt, True)
        is_start = datetime.datetime.now()
        isRslt = is_helper.IS_Access()

        isRetStatus = ISReturnStatus.SEARCH_OK
        isRetInfo = ISReturnInfo(0, 0, [])
        isRetProd = ISReturnProduct([])

        isRslt = ISSearchResult(isRetStatus, isRetInfo, isRetProd)

        splogger.debug(isRslt)
        is_end = datetime.datetime.now()
        splogger.debug("Done search, respone time {}".format((is_end - is_start)))
        splogger.debug("==== Step 2. IS Access Success ====")

        # step 3. 拼装结果
        ''' IS Result
        enum ISReturnStatus{
            SEARCH_OK,
            ERROR_NO_COMP_ID,
            ERROR_NO_CRAFT_ID
        }
        
        struct ISReturnInfo{
            1: required i32	       srch_img_cnt;
            2: required i32	       srch_sample_cnt;
            3: optional list<string> debug_info;
        }
        
        struct ISReturnProduct{
            1: required list< list<i32> > list_prods;
        }
        // 注: 一次查询可能包含多个检索图片
        
        struct ISSearchResult{
            1: required ISReturnStatus  ret_status;
            2: required ISReturnInfo	ret_info;
            3: required ISReturnProduct ret_prod;
        }
        '''

        ''' SP Result 
        enum SPReturnStatus{
            SEARCH_OK,
            ERROR_1
        }
        
        struct SPReturnInfo{
            1: required i32	       srch_img_cnt;
            2: required i32	       srch_sample_cnt;
            3: optional list<string> debug_info;
        }
        
        struct SPReturnProduct{
            1: required list< list<i32> > list_prods;
        }
        
        struct SPSearchResult{
            1: required SPReturnStatus  ret_status;
            2: required SPReturnInfo	  ret_info;
            3: required SPReturnProduct ret_prod;
        }
        '''
        if isRslt.ret_status == ISReturnStatus.SEARCH_OK:
            sp_status = SPReturnStatus.SEARCH_OK
        else:
            sp_status = SPReturnStatus.ERROR_1
        retInfo = SPReturnInfo(isRslt.ret_info, isRslt.ret_info.srch_sample_cnt, isRslt.ret_info.debug_info)
        retProd = SPReturnProduct(isRslt.ret_prod.list_prods)
        srch_rslt = SPSearchResult(sp_status, retInfo, retProd)

        return srch_rslt

    def _debugInfo(self, req):
        splogger.debug(req)
