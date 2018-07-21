#image search app
图像搜索

# TODO
* searcher部分
* 没有做容错: 例如 判断图片是否可以解析成jpg格式,完整图片; 参数校验等等
* util工具类需要优化一下: 最好整理出来日志类["access日志" 和 "错误或者Debug信息日志"]和配置类
* 从样本子图到样品图的合并, 以及排序, 需要正排信息做排序. 但目前在考虑在Searcher做还是SP做排序,
    同时可能需要redis作为正排索引工具
* 整体代码优化: 例如直接将QP布置为tensorflow serving
* 离线流程开发

# DONE
* docker准备
** SP 只需要thrift环境, 不需要docker
** QP 需要准备tensorflow的docker环境
     但centos可以直接安装virtualenv, 然后安装tensorflow以及thrift安装包;
** search 需要准备faiss的docker环境, 目前已经准备好了
* SP 到 QP 访问
** SP 主要功能
** QP 主要功能
**
