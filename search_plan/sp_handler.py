# coding: utf-8

import sys
# my custom utility
from util.util import *
from idls.sp_idl.idl_search_plan.ttypes import *

class SearchPlanServiceHandler:

    def doImageSearch(self, req):
        splogger.debug("Get one request")
        start = datetime.datetime.now()

        # search function
        ret = self._doImageSearch(req)

        final_end = datetime.datetime.now()
        splogger.debug("Done search, respone time {}".format((final_end - start)))

    def _doImageSearch(self, req):
        srch_rslt = SearchResult

        # step 1. query_process

        # step 2. vector_search

        # step 3.

        return srch_rslt
