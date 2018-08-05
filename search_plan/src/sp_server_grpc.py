# coding: utf-8

"""
file  : sp_server
desc  : 
author: danny
date  : 2018-07-15 
"""
import sys, time
import grpc
from    concurrent import futures

from idls.sp_idl_grpc.search_plan import rpc_searcher_plan_pb2
from idls.sp_idl_grpc.search_plan import rpc_searcher_plan_pb2_grpc

from util.util import *
from sp_handler_grpc import SearchPlanServiceGRPCHandler

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    rpc_searcher_plan_pb2_grpc.add_SearchPlanServiceServicer_to_server(SearchPlanServiceGRPCHandler(), grpcServer)
    grpcServer.add_insecure_port(sp_conf["services"]["sp"]["ip"] + ':' + str(sp_conf["services"]["sp"]["port"]))
    grpcServer.start()
    splogger.info("SP start at {} and port {}".format(sp_conf["services"]["sp"]["ip"], sp_conf["services"]["sp"]["port"]))
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    serve()
