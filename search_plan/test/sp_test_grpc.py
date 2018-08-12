# coding: utf-8
import os, sys
cur_path = os.getcwd()
sys.path.append(cur_path+"/../src")

import grpc
from util.util import *

from idls.sp_idl_grpc.search_plan import rpc_searcher_plan_pb2
from idls.sp_idl_grpc.search_plan import rpc_searcher_plan_pb2_grpc

def Test_SP():
    splogger.debug("Begin test")
    ''' 
    message SPRequest{
        enum SPRequestType{
            IMAGE_SEARCH = 0;
            SEARCH_DEBUG = 1;
        }
        SPRequestType   type  =   1;
        int32		    comp_id = 2;
        int32		    craft_id= 3;
        repeated int32	styles  = 4;
        repeated string img_urls= 5;
        map<string, string> srch_params = 6;
    }
    '''
    img_urls = []
    #img_urls.append('/Users/danny/Documents/devenv/tf_vir/workspace/imagesearch/data/test_data/IMG_3592.JPG')
    #img_urls.append('/Users/danny/Documents/devenv/tf_vir/workspace/imagesearch/data/test_data/IMG_3594.JPG')
    img_urls.append('/home/admin/projectspace/test/search_test/test_images/IMG_3592.JPG')
    img_urls.append('/home/admin/projectspace/test/search_test/test_images/IMG_3594.JPG')
    params = {}
    params['debug'] = "1"
    spReq = rpc_searcher_plan_pb2.SPRequest(type=0, comp_id=1, craft_id=1,
                                            styles=[1,2], img_urls=img_urls,
                                            srch_params=params)
    splogger.debug(spReq)

    conn = grpc.insecure_channel("47.99.45.134" + ':' + str(3207))
    #conn = grpc.insecure_channel("localhost" + ':' + str(3207))
    sp_client = rpc_searcher_plan_pb2_grpc.SearchPlanServiceStub(channel=conn)
    spRslt = sp_client.doImageSearch(spReq)
    splogger.info("Sp return")
    splogger.info(spRslt)


if __name__ == '__main__':
    Test_SP()
