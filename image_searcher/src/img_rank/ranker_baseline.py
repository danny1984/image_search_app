# coding: utf-8
import redis
from  util.util import *

class redisDatabase:
    def __init__(self):
        #self.host = 'localhost'
        self.host = '127.0.0.1'
        self.port = 6379

    def write(self,img_id,sample_id,style_id_list=[]):
        try:
            key = img_id
            value = []
            value.append(sample_id)
            value.append(style_id_list) #val = [sample_id,[style_id,...]] 实际变成了 字符串了，并不是 []存储在 redis中
            r = redis.StrictRedis(host=self.host,port=self.port)
            r.set(key,value)
        except Exception, exception:
            islogger.info(exception)

    def read(self,img_id):
        try:
            key = img_id
            r = redis.StrictRedis(host=self.host,port=self.port)
            value = r.get(key)
            islogger.debug(value)
            return value
        except Exception, exception:
            islogger.info(exception)

# class RankerBaseline:
#     def __init__(self):
#         self._name = "baseline"
#
#     # query_vecs = req.query_vecs
#     # img_dis, img_name = index_info.doSearch(query_vecs, top_k)
#     # # TODO: 排序
#     # # prod_name, prod_dis = RankerBaseline(img_dis, img_name, req)

def RankerBaseline(img_dis, img_name, req):
    #return img_name, img_dis
    islogger.debug("In ranking")
    #建立的内存数据库redis，默认 db=0
    #TODO: 最好改成类, 只初始化一次
    redisDB = redisDatabase() #初始化

    prod_name=[]
    prod_dis=[]
    for row in range(0,len(img_name)): #每一row 代表 一个图片的搜索结果
        sample_StylesDises_dict = {}  # 采用字典{ sample_id : [ [style1,style2,...], [dis1,dis2,dis3,...] ] }，相同sample_id聚合

        for col in range(0,len(img_name[row])):#当前行中每一个 imgID
            imgID = img_name[row][col]
            result = redisDB.read(imgID)  # redis存储结构 img_id:[sample_id,[style_id,...]]
            #TODO: 需要保护一下 无法查到
            result = result.replace('[','')
            result = result.replace(']', '')
            result = result.split(',')
            numbers = [long(x) for x in result] #将字符串转为数字

            sampleID = numbers[0]
            styleIDs = numbers[1:] #redis存储结构 img_id:[sample_id,[style_id,...]]
            try:
                key = sampleID           # redis 取出 img_id 对应的 sample_id ，redis存储结构 img_id:[sample_id,[style_id,...]]
                # key不存在，则新建，若已存在，则追加
                if key not in sample_StylesDises_dict:
                    value = []
                    value.append(styleIDs) #value 第0个元素
                    v = [] #value第 1 个元素 初始
                    v.append(img_dis[row][col])
                    value.append(v)
                    sample_StylesDises_dict[key] = value  #{ sample_id : [ [style1,style2,...], [dis1,dis2,dis3,...] ] }

                else: #已经存在，需要合并 key
                    sample_StylesDises_dict[key][1].append(img_dis[row][col]) #只修改 dis部分
            except: Exception,"sample_id error"

        #本行 kv 聚合结束 sample_StylesDises_dict = { sample_id : [ [style1,style2,...], [dis1,dis2,dis3,...] ] }
        islogger.debug("sample_StylesDises_dict result")
        islogger.debug(sample_StylesDises_dict)

        dis_name=[]
        for id in sample_StylesDises_dict:
            try: #计算 sample_id对应的平均距离
                mean_dis = sum(sample_StylesDises_dict[id][1])/len(sample_StylesDises_dict[id][1]) #第1项为 距离列表，第0项为类型列表
                dis_name.append( (mean_dis,id) )
            except: Exception,"divided by zero"

        ## 单行 均值距离计算完成
        disStyle_name = []  #考虑 风格之后的 搜索距离-样品 列表
        ALL_SELECTED_CODE = 0 # 风格 全选时的 style_id 取值
        STYLE_DISTANCE = 10000 #无任何风格被选中 时的 距离加成
        for x in range(0,len(dis_name)):  # dis_name = [(mean_dis,id),(),,,]
            id=dis_name[x][1]
            styleIDs = sample_StylesDises_dict[id][0] #{ sample_id : [ [style1,style2,...], [dis1,dis2,dis3,...] ] }

            name = dis_name[x][1]
            disStyle = dis_name[x][0]  # disStyle默认为 dis_name对应值，除非 由于style而作修正

            ##根据styles对相似距离disStyle进行修正
            for i in range(0,len(styleIDs)):  # styleIDs[] 与 req 的 档位关系, sytle_id 来自 搜索库，req来自请求，应该采用 搜索结果 匹配 req
                style = styleIDs[i] #取出 sample_StylesDises_dict 表中 的风格代码
                styleList_req = req.styles  #取出查询数据中 选中的 风格列表
                if (style in styleList_req) or (ALL_SELECTED_CODE in styleList_req):
                    #disStyle_name.append(dis_name[x])
                    disStyle = disStyle #若 搜索结果风格 包含在 请求风格列表中 或者 请求列表风格全选，则保持 距离不变
                else:
                    #disStyle_name.append( (dis_name[x][0] + STYLE_DISTANCE,dis_name[x][1]) ) #风格不符合，则 搜素距离 加长
                    disStyle = disStyle + STYLE_DISTANCE  #风格不符合，则 搜素距离 加长

            #添加修正后的 disStyle_name
            disStyle_name.append((disStyle, name))
        # 考虑 风格之后的 搜索距离-样品 列表 disStyle_name 按照 搜索距离排序
        disStyle_name_sorted = sorted(disStyle_name)

        #将 排序后的 dis-name 分别存到 本行的 列表中
        row_prod_name = [] #存放单张搜索结果 的sample_id
        row_prod_dis = []  #存放单张搜索结果 sample_id 对应 的搜索距离
        for x in disStyle_name_sorted:
            row_prod_dis.append(x[0])
            row_prod_name.append(x[1])

        prod_name.append(row_prod_name) #将每一行即 单张 的搜索结果 加入 总体搜索结果
        prod_dis.append(row_prod_dis)
        islogger.debug("Rank result")
        islogger.debug(prod_name)
        islogger.debug(prod_dis)

    #得到 prod_name[][] prod_dis[][]
    return  (prod_name, prod_dis)




