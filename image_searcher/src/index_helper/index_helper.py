# coding: utf-8
# 所有图片索引接口
import json as js
from vec_index import *

class IndexHelper:
    def __init__(self, conf, logger):
        self._conf      = conf
        self._logger    = logger
        self._index_sum = {}

    def IndexHelper(self, isCheck=False):
        return self._IndexHelper(isCheck)

    def _IndexHelper(self, isCheck):
        vector_conf_path = self._conf["project_home_path"] + "./conf/" + self._conf["vector_conf_home"]
        self._logger.info("Load vector conf {}".format(vector_conf_path))

        with open(vector_conf_path, "r") as vector_conf_fin:
            vector_conf = js.load(vector_conf_fin)
            self._logger.info("Total {} companies and {} indexs".format(
                                                        vector_conf["index_info"]["comp_cnt"],
                                                        vector_conf["index_info"]["index_cnt"]))

            for (index_id, index_info) in vector_conf.items():
                if index_id == "index_info":
                    continue
                comp_id = index_info["comp_id"]
                craft_id= index_info["craft_id"]
                vec_dir_home = index_info["vector_dir_home"]
                self._logger.info("Load Index {} for company {}, craft {}, and dir {}".format(index_id,
                                                      comp_id, craft_id, vec_dir_home))
                tmp_index_info = VectorIndex(index_id, index_info, self._logger, isCheck)
                if isCheck:
                    continue

                if self._index_sum.has_key(comp_id):
                    if self._index_sum[comp_id].has_key(craft_id):
                        self._index_sum[comp_id][craft_id] = tmp_index_info
                    else:
                        self._index_sum[comp_id][craft_id] = tmp_index_info
                else:
                    self._index_sum[comp_id] = {}
                    self._index_sum[comp_id][craft_id] = tmp_index_info

        return self._index_sum
