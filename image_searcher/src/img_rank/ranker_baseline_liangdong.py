# coding: utf-8

# # ======================================================================================================
# img_name = [[1179, 1180, 1182, 1183, 1184],
#             # img_id 1179,1180 = sample_id 271 = style_id 4, img_id 1182,1183,1184 = sample_id 272 = style_id 4
#             [1179, 1180, 1182, 1183, 1184],
#             [1179, 1180, 1182, 1183, 1184],
#             [1179, 1180, 1182, 1183, 1184],
#             [1179, 1180, 1182, 1183, 1184],
#             [1179, 1180, 1182, 1183,
#              1184]]  # <type 'tuple'>: (508L, 271L, 4, datetime.datetime(2018, 8, 23, 7, 5, 40), datetime.datetime(2018, 8, 23, 7, 5, 40))
# # <type 'tuple'>: ((509L, 272L, 4, datetime.datetime(2018, 8, 23, 7, 9, 4), datetime.datetime(2018, 8, 23, 7, 9, 4)),)
# img_dis = [[0.1, 0.3, 0.1, 0.2, 0.6],  # 按照原始搜索结果 271, 272
#            [0.1, 0.3, 0.1, 0.2, 0.1],  # 按照原始搜索结果 272, 271
#            [0.1, 0.3, 0.1, 0.2, 0.6],  # 按照原始搜索结果 271, 272
#            [0.1, 0.3, 0.1, 0.2, 0.1],  # 按照原始搜索结果 272, 271
#            [0.1, 0.3, 0.1, 0.2, 0.6],  # 按照原始搜索结果 271, 272
#            [0.1, 0.3, 0.1, 0.2, 0.1], ]  # 按照原始搜索结果 272, 271
# req = [[2, 3],  # 无风格被选中，距离全部加长，但与原始搜索结果相比，排序不变
#        [2, 3],
#        [0],  # 默认分割全选，搜索距离不变，排序不变
#        [0],
#        [1, 4],  # 风格4被选中，搜索距离会受风格档位的影响
#        [1, 4]]

class RankerBaseline:
    def __init__(self):
        self._name = "baseline"

    def __init__(self,img_dis, img_name, req):
        self._name = "baseline"

        ## mysql 属性数据库配置
        # mysql_host = 'rm-bp1iw6jmy10og8w5r.mysql.rds.aliyuncs.com'   # 内网地址，远程主机的ip地址
        mysql_host = 'rm-bp1iw6jmy10og8w5ruo.mysql.rds.aliyuncs.com'  # 外网地址，远程主机的ip地址
        mysql_user = 'tujing_read'  # MySQL用户名
        mysql_passwd = 'sl677JsYs'  # 用户密码
        mysql_db = 'tujing'  # database名
        mysql_port = int(3306)  # 数据库监听端口，默认3306，整型数据
        mysql_charset = 'utf8'  # 指定utf8编码的连接
        mysql_conn = MySQLdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_db, mysql_port, mysql_charset)
        mysql_cursor = mysql_conn.cursor()  # 创建一个光标，然后通过光标执行sql语句

        prod_name=[]
        prod_dis=[]
        for row in range(0,len(img_name)): #每一row 代表 一个图片的搜索结果
            sample_dises_dict={}  #采用字典{ sample_id : [dis1,dis2,...] }，相同sample_id聚合
            for col in range(0,len(img_name[row])):
                id = img_name[row][col]
                mysql_cursor.execute( ' select sample_id from tujing.sample_imgs  where tujing.sample_imgs.img_id= {0} '.format(id))
                sample_id = mysql_cursor.fetchall()  # 取出cursor得到的数据
                try:
                    key = sample_id[0][0]           # 取出 img_id 对应的 sample_id ，此处 sample_id 结果是个二维数组
                    # key不存在，则新建，若已存在，则追加
                    if key not in sample_dises_dict:
                        value = []
                        value.append(img_dis[row][col])
                        sample_dises_dict[key] = value
                    else:
                        sample_dises_dict[key].append(img_dis[row][col])
                except: Exception,"sample_id error"

            #本行 kv 聚合结束 sample_dises_dict = {sample_id: [dis1, dis2, ...]}
            dis_name=[]
            for id in sample_dises_dict:
                try: #计算 sample_id对应的平均距离
                    mean_dis = sum(sample_dises_dict[id])/len(sample_dises_dict[id])
                    dis_name.append( (mean_dis,id) )
                except: Exception,"divided by zero"

            ## 单行 均值距离计算完成
            disStyle_name = []  #考虑 风格之后的 搜索距离-样品 列表
            ALL_SELECTED_CODE = 0 # 风格 全选时的 style_id 取值
            STYLE_DISTANCE = 10000 #无任何风格被选中 时的 距离加成
            for x in range(0,len(dis_name)):
                #mysql_cursor.execute( ' select * from tujing.sample_styles join ( select sample_id from tujing.sample_imgs  where tujing.sample_imgs.img_id= {0} ) as A on A.sample_id= tujing.sample_styles.sample_id '.format(id))
                id=dis_name[x][1]
                mysql_cursor.execute( ' select style_id from tujing.sample_styles  where tujing.sample_styles.sample_id= {0} '.format(id))
                style_id = mysql_cursor.fetchall()  # 取出cursor得到的数据
                for i in range(0,len(style_id)):  # style_id[][] 与 req 的 档位关系, sytle_id 来自 搜索库，req来自请求，应该采用 搜索结果 匹配 req
                    style = style_id[i][0] #取出 sample_style 表中 的风格代码
                    styleList_req = req[row]  #取出查询数据中 选中的 风格列表
                    if (style in styleList_req) or (ALL_SELECTED_CODE in styleList_req):
                        disStyle_name.append(dis_name[x]) #若 搜索结果风格 包含在 请求风格列表中 或者 请求列表风格全选，则保持 距离不变
                    else:
                        disStyle_name.append( (dis_name[x][0] + STYLE_DISTANCE,dis_name[x][1]) ) #风格不符合，则 搜素距离 加长

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

        #得到 prod_name[][] prod_dis[][]
        return  prod_name, prod_dis






