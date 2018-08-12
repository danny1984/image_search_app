# coding: utf-8

import oss2
import os, sys


class OSSHelper:

    def __init__(self, conf):
        self._conf      = conf
        self._id        = conf["oss_conf"]["id"]
        self._secret    = conf["oss_conf"]["secret"]
        self._auth      = oss2.Auth(self._id, self._secret)
        self._bucket    = oss2.Bucket(self._auth, self._conf["oss_conf"]["end_name"],
                                      self._conf["oss_conf"]["bucket_name"])
        self._local_dir = conf["oss_conf"]["local_file_dir"]


    def getOSSFile(self, key):
        local_image_path = self._local_dir + key
        if os.path.exists(local_image_path):
            return local_image_path
        self._bucket.get_object_to_file(key, local_image_path)
        return local_image_path


#conf = {}
#conf["oss_conf"] = {}
#conf["oss_conf"]["id"] = 'LTAIOhsKagLIaskD'
#conf["oss_conf"]["secret"] = 'b507nOLWAwwfwIB4l2cEAcZCyJ3Q5h'
#conf["oss_conf"]["end_name"] = 'oss-cn-hangzhou.aliyuncs.com'
#conf["oss_conf"]["bucket_name"] = 'tujing-clothimage'
#conf["oss_conf"]["local_file_dir"] = '/Users/danny/Downloads/'
#
#osshelper = OSSHelper(conf)
#key = ''
#print osshelper.getOSSFile('1/9123cf19e13847b7b17ff87941b44464.JPG')
