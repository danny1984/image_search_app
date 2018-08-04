# coding: utf-8
"""
sp_test.py
"""
import os, sys
cur_path = os.getcwd()
sys.path.append(cur_path+"/../src")

from util.util import *

from idls.sp_idl.search_plan import SearchPlanService
from idls.sp_idl.search_plan.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol

try:
    transport = TSocket.TSocket('localhost', 3207)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    client = SearchPlanService.Client(protocol)
    transport.open()

    splogger.info("Sp access");
    '''
    enum RequestType
    {
        IMAGE_SEARCH,
        SEARCH_DEBUG
    }
    struct Request
    {
        1: required RequestType type;
        2: required i32         comp_id;
        3: required i32         craft_id;
        4: required set < i32 > styles;
        5: required list < string > img_urls;
        6: optional map < string, string > srch_params;
    }
    '''
    styles   = set([1,2])
    img_urls = []
    img_urls.append('/Users/danny/Documents/devenv/tf_vir/workspace/imagesearch/data/test_data/IMG_3592.JPG')
    img_urls.append('/Users/danny/Documents/devenv/tf_vir/workspace/imagesearch/data/test_data/IMG_3594.JPG')
    params = {}
    params['debug'] = "1"
    req = SPRequest(0, 1, 1, styles, img_urls, params)

    rslt = client.doImageSearch(req)
    splogger.info("Sp return")
    splogger.info(rslt)

    transport.close()

except Thrift.TException, ex:
    print "%s" % (ex.message)