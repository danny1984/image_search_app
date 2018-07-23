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
    1. SP 只需要thrift环境, 不需要docker
    2. QP 需要准备tensorflow的docker环境
       但centos可以直接安装virtualenv, 然后安装tensorflow以及thrift安装包;
    3. search 需要准备faiss的docker环境, 目前已经准备好了

* SP 到 QP 访问
    1. SP 主要功能
    2. QP 主要功能

# 数据
* 公司名/风格/工艺 都转换成id [每种类型重新编号],

* Image: (图片id int, 样品id int, 图片地址 string, 工艺id int, 风格id int多值字段, create_time datetime, modify_time datetime)
    1. 每家公司 每种工艺 图片id 可以重新编号

# 外部对SP的接口RPC
*  接口文件 idl_search_plan.thrift
    // ========   Request  ==========
    enum SPRequestType{
        IMAGE_SEARCH,
        SEARCH_DEBUG
    }

    struct SPRequest{
        1: required SPRequestType type;
        2: required i32		comp_id;
        3: required i32		craft_id;
        4: required set<i32>	styles;
        5: required list<string> img_urls;
        6: optional map<string, string> srch_params;
    }
    .....