# coding: utf-8
import sys, os
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

class VectorGen:
    def __init__(self, conf, logger):
        self._conf   = conf
        self._logger = logger
        self._load_inception_model(conf)

    def gen_vector(self, listImage):
        listVectors = []

        with tf.Session() as sess:
            init = tf.global_variables_initializer()
            sess.run(init)

            for img_path in listImage:
                self._logger.debug("To generate vector for image: {}".format(img_path))
                image_data = gfile.FastGFile(img_path, 'rb').read()
                bottleneck_values = self._run_bottleneck_on_image(sess, image_data, self.jpeg_data_tensor, self.bottleneck_tensor)
                listVectors.append(bottleneck_values)

        return listVectors

    def _load_inception_model(self, conf):   # 读取模型
        self._logger.info("Load inception v3 model: {} {}".format(conf['inception_v3']['model_dir'], conf['inception_v3']['model_file']))
        with gfile.FastGFile(os.path.join(conf['inception_v3']['model_dir'], conf['inception_v3']['model_file']), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        # 加载模型，返回对应名称的张量
        self.bottleneck_tensor, self.jpeg_data_tensor = tf.import_graph_def(graph_def,
                                                                      return_elements=[conf['inception_v3']['bottleneck_data_name'],
                                                                                        conf['inception_v3']['image_data_name']])

    def _run_bottleneck_on_image(self, sess, image_data, image_data_tensor, bottleneck_tensor):
        bottleneck_values = sess.run(bottleneck_tensor, {image_data_tensor: image_data})
        bottleneck_values = np.squeeze(bottleneck_values)
        return bottleneck_values


