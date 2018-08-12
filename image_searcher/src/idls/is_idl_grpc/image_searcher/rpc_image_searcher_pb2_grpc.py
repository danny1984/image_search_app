# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import rpc_image_searcher_pb2 as rpc__image__searcher__pb2


class ImageSearcherServiceStub(object):
  """=======   Service  ===========
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.doSearch = channel.unary_unary(
        '/image_searcher.ImageSearcherService/doSearch',
        request_serializer=rpc__image__searcher__pb2.ISRequest.SerializeToString,
        response_deserializer=rpc__image__searcher__pb2.ISSearchResult.FromString,
        )


class ImageSearcherServiceServicer(object):
  """=======   Service  ===========
  """

  def doSearch(self, request, context):
    """service function
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ImageSearcherServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'doSearch': grpc.unary_unary_rpc_method_handler(
          servicer.doSearch,
          request_deserializer=rpc__image__searcher__pb2.ISRequest.FromString,
          response_serializer=rpc__image__searcher__pb2.ISSearchResult.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'image_searcher.ImageSearcherService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))