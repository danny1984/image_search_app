# coding: utf-8

"""
file  : is_server
desc  : 
author: danny
date  : 2018-07-22 
"""

import sys, time
import grpc
from    concurrent import futures

from idls.is_idl_grpc.image_searcher import rpc_image_searcher_pb2
from idls.is_idl_grpc.image_searcher import rpc_image_searcher_pb2_grpc
from util.util import *
from is_handler_grpc import ImageSearcherServiceGRPCHandler

_ONE_YEAR_IN_SECONDS = 60 * 60 * 24 * 365

def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    rpc_image_searcher_pb2_grpc.add_ImageSearcherServiceServicer_to_server(ImageSearcherServiceGRPCHandler(is_conf, islogger), grpcServer)
    grpcServer.add_insecure_port(is_conf["services"]["is"]["ip"] + ':' + str(is_conf["services"]["is"]["port"]))
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_YEAR_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    serve()
