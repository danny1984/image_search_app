# coding: utf-8

# 图片索引详情类

import sys
import os, glob
import numpy as np
import faiss

class VectorIndex:
    def __init__(self, index_id, index_conf, logger, isCheck=False):
        self._index_id      = index_id
        self._index_conf    = index_conf
        self._comp_id       = index_conf["comp_id"]
        self._craft_id      = index_conf["craft_id"]
        self._vec_dir_home  = index_conf["vector_dir_home"]
        self._VECTOR_DIM    = index_conf["dim"]
        self._imgname_to_id = {}
        self._id_to_imgname = [] # np.array
        self._imgvecs       = []
        self._logger        = logger
        self._index         = self._vector_2_index(isCheck)
        self._logger.info("=== Comp_id {} and craft {} index build successfully".format(self._comp_id, self._craft_id))

    def doSearch(self, query_vecs, topk):
        self._logger.info(type(query_vecs))
        query_vecs = np.array(query_vecs, dtype=np.float32)
        img_dis, img_idxs = self._index.search(query_vecs, topk)
        # 遍历所有查询
        img_distances = [] # 二维数组, 存储多个距离 可能多个query
        img_names = [] # 二维数组, 存储多个名称
        for (dis, idx) in zip(img_dis, img_idxs):
            # 通过索引获取返回结果
            img_names.append(self._id_to_imgname[idx].tolist())
            img_distances.append(dis.tolist())

        # #这里直接返回img_name
        # img_name = []
        # for return_idx, img_idx in enumerate(img_idxs):
        #     if self._id_to_imgname.has_key(img_idx):
        #         img_name.append(self._id_to_imgname[img_idx])
        #     else:
        #         # 删除不存在的图片的距离
        #         img_dis.remove(return_idx)
        return img_distances, img_names

    def _vector_2_index(self, isCheck):
        # step 1: 产生 _imgvecs, _id_to_imgname, _imgname_to_id
        imgvecs = self._load_image_vector(isCheck)
        # step 1: 如果是check 则不build索引 直接返回了
        if isCheck and len(imgvecs) == 0:
            index = faiss.IndexFlatL2(self._VECTOR_DIM)
            return index
        # step 2: 创建索引
        return self._build_image_index(imgvecs)

    def _build_image_index(self, imgvecs):
        np_imgvecs = np.array(imgvecs, dtype=np.float32)

        index = faiss.IndexFlatL2(self._VECTOR_DIM)
        self._logger.debug("Index is_trained: " + str(index.is_trained))

        index.add(np_imgvecs)
        self._logger.debug("Index total: " + str(index.ntotal))

        return index

    def _load_image_vector(self, isCheck):
        self._logger.info("Load vector from {}".format(self._vec_dir_home))
        vecfile_glob = os.path.join(self._vec_dir_home, '*.txt')
        imgvec_files = glob.glob(vecfile_glob)

        image_index_name = []
        for idx, imgvec_file in enumerate(imgvec_files):
            file_base_name = os.path.basename(imgvec_file)
            imgname = file_base_name.replace(".txt", "")
            image_index_name.append(imgname)
            self._imgname_to_id[imgname] = idx
            with open(imgvec_file) as fin:
                vec_str = fin.readline()
                imgvec = [float(x) for x in vec_str.split(",")]

                if isCheck:
                    if self._VECTOR_DIM != len(imgvec):
                        self._logger.info("ImgEmbedding size error!")
                        self._imgvec=[]
                        return self._imgvec
                    else:
                        continue

                self._imgvecs.append(imgvec)
                #self._logger.info( str(idx) + " : " + imgname + " : " + ",".join([str(x) for x in imgvec[:5]]) )
        if isCheck:
            return self._imgvecs
        # TODO: 改成 numy 数组直接索引
        self._id_to_imgname = np.array(image_index_name)

        assert len(self._imgvecs) == len(self._imgname_to_id)
        assert self._VECTOR_DIM == len(self._imgvecs[0])

        self._logger.debug("Read " + " " + str(len(self._imgname_to_id)) + " files!")
        self._logger.debug("Image vector dim: " + str(len(self._imgvecs[0])))
        return self._imgvecs
