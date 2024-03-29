
#遗传算法，为最后一层生成参数
#输出：
#第一个参数这个影集照片数量，第二个参数是一个数组 第i项代表第i张图片的gif数量，第三个参数是一个数组，第i项是第i个gif 的id（现在是地址），(第四个参数是规定尺寸
# 第五个参数是规定位置，这个可以根据id一起取？最后再说吧，不行就三个参数是地址 尺寸位置)最后一个参数是音乐的卡点时间

#输入数据格式：
import random
from . import cost_calculate as cc
import xlrd
import functools
from . import generate
import copy
from . import get_tempalte

from .filelist import *
from .templates import total_photo_template,openning_templates,photo_with_poem_templates,ending_templates

pt="./movie/modules/assets/gifs/" #资源文件目录
xls_file= r"./movie/modules/assets/gifs/info.xls" #xls文件

#加载图片类
class picture:
    def __init__(self,_color,_factor,_weather,_path):
        picture.color=_color
        picture.factor=_factor
        picture.path=_path
        picture.weather=_weather
def pic_lodain(picture_number):
    photos=[]
    photo=picture()

#gif数据库装入缓存的定义
class one_giftem:
    def __init__(self,_id,_factor,_size,_position,_path,_color,_weather):
        self.id=_id
        self.factor=_factor
        self.size=_size
        self.position=_position
        self.path=_path
        self.color=_color
        self.weather=_weather

#全局变量  和  参数定义：
pictures=[]
#apicture=picture()
#pictures.append(apicture)#加载入图片类

k=10 #模板的数量
p_allgif_t=10
p_allgif_i=3 # p_allgif_i / p_allgif_t gif的产生率 对于初代而言
all_gif=[]#gif表装入内存
#a=one_giftem()
#all_gif.append(a)

Gene_mutation_t=1000
Gene_mutation_i=200
#变异率 Gene_mutation_i / Gene_mutation_t
Gene_mutation_no=3#最大的变异点位数

#
firsit_num=50#初代目的数量
select_num=20
theta_score=10#收敛阈值

#最大的迭代次数
ctrl_times=100



#模板类的定义
# 模板类的定义
class gif_Template:
    # 构造函数用于生成初代：
    def __init__(self, photo_num, ini,temp=[]):
        self.template=[] #模板列表 第 i项是 第 i个模板的id
        self.backgroud=[] #背景图列表 第 i项是 第i张背景图
        self.pic_num = photo_num;  # 图片数量
        self.gif_num = []  # gif数量（数组）  新版本是针对模板来
        self.path = []  # 路径
        self.size = []
        self.position = []
        self.color = []
        self.weather = []
        self.factor = []
        self.scores = 0

        # 提示要初始化的时候才进行
        if ini != 0:
            self.template=temp
            #get_tempalte.gene_gif_main()    ###

            
            #给每个模板挨个匹配gif
            for i in range(0, len(self.template)):
                self.gif_num.append(0)
                p_allgif = random.randint(0, p_allgif_t)
                if p_allgif < p_allgif_i:
                    self.gif_num[i] = self.gif_num[i] + 1
                    gif_no = random.randint(1, k)
                    self.path.append(all_gif[gif_no].path)
                    self.size.append(all_gif[gif_no].size)
                    self.position.append(all_gif[gif_no].position)
                    self.color.append(all_gif[gif_no].color)
                    self.weather.append(all_gif[gif_no].weather)
                    self.factor.append(all_gif[gif_no].factor)

        # ...用于不同位置的模板这里还可以加

    # 变异
    # 编码方式：整数编码（会不会因为这个效果不好呢/疑问）
    def Gene_mutation(self):
        p_mutation = random.randint(0, Gene_mutation_t)
        if p_mutation < Gene_mutation_i:  # 变异概率
            times = random.randint(0, Gene_mutation_no)  # 变异的点位数
            for i in range(0, times):
                point_no = len(self.path)
                if point_no!=0:
                    point = random.randint(0, point_no - 1)

                    mutation_point = random.randint(1, k)
                    self.path[point] = all_gif[mutation_point].path
                    self.size[point] = all_gif[mutation_point].size
                    self.position[point] = all_gif[mutation_point].position
                    self.color[point] = all_gif[mutation_point].color
                    self.factor[point] = all_gif[mutation_point].factor
                    self.weather[point] = all_gif[mutation_point].weather
    # 适应性函数
    def gif_fit(self):
        number = len(self.template)
        cost = 0
        gif_no = 0  # gif编号
        pic_no = 0  # picture编号
        #print(self.gif_num)
        #print(number)
        #print(self.template)
        for i in range(0, number):
            for t in range(0, self.gif_num[i]):
                for y in range(0,total_photo_template[self.template[i]]):
                    cost = cost + cc.color_weight * cc.color(pictures[pic_no].color, self.color[gif_no])
                    cost = cost + cc.factor_weight * cc.factor(pictures[pic_no].factor, self.factor[gif_no])
                    cost = cost + cc.weather_weight * cc.weather(pictures[pic_no].weather, self.weather[gif_no])
                    cost = cost + cc.chongfu(self)
                    #print("cost")
                    #print(cost)
                    pic_no=pic_no+1
                pic_no=pic_no-total_photo_template[self.template[i]]
                gif_no = gif_no + 1
        return cost

    def __lt__(self, other):
        return self.scores < other.scores

#交叉产生下一代
#重写函数：
def Gene_breed(sequence_a,sequence_b):
    if len(sequence_a.template)==1:
        return sequence_b
    if len(sequence_b.template)==1:
        return sequence_a
    new_breed=gif_Template(sequence_a.pic_num,0)
    new_breed.template=copy.deepcopy(sequence_a.template[:])
    the_number1=len(sequence_a.gif_num)
    the_number=min(len(sequence_a.gif_num),len(sequence_b.gif_num))

    _point_a=random.randint(1,the_number-1)
    _point_b=random.randint(1,the_number-1)
    point_a=min(_point_a,_point_b)
    point_b=max(_point_a,_point_b)

    new_breed.gif_num = sequence_a.gif_num[0:point_a] + sequence_b.gif_num[point_a:point_b] + sequence_a.gif_num[
                                                                                              point_b:the_number1]

    number_a_a = [sequence_a.gif_num[0]]
    number_b_b = [sequence_b.gif_num[0]]
    for i in range(0, the_number1 - 1):
        number_a_a.append(number_a_a[i] + sequence_a.gif_num[i + 1])
    for i in range(0, the_number - 1):
        number_b_b.append(number_b_b[i] + sequence_b.gif_num[i + 1])
    new_breed.color = sequence_a.color[0:number_a_a[point_a - 1]] + sequence_b.color[
                                                                    number_b_b[point_a - 1]:number_b_b[
                                                                        point_b - 1]] + sequence_a.color[
                                                                                        number_a_a[point_b - 1]:
                                                                                        number_a_a[the_number1 - 1]]

    new_breed.weather = sequence_a.weather[0:number_a_a[point_a - 1]] + sequence_b.weather[
                                                                        number_b_b[point_a - 1]:number_b_b[
                                                                            point_b - 1]] + sequence_a.weather[
                                                                                            number_a_a[point_b - 1]:
                                                                                            number_a_a[
                                                                                                the_number1 - 1]]
    new_breed.factor = sequence_a.factor[0:number_a_a[point_a - 1]] + sequence_b.factor[
                                                                      number_b_b[point_a - 1]:number_b_b[
                                                                          point_b - 1]] + sequence_a.factor[
                                                                                          number_a_a[point_b - 1]:
                                                                                          number_a_a[
                                                                                              the_number1 - 1]]
    new_breed.path = sequence_a.path[0:number_a_a[point_a - 1]] + sequence_b.path[
                                                                  number_b_b[point_a - 1]:number_b_b[
                                                                      point_b - 1]] + sequence_a.path[
                                                                                      number_a_a[point_b - 1]:
                                                                                      number_a_a[the_number1 - 1]]
    new_breed.position = sequence_a.position[0:number_a_a[point_a - 1]] + sequence_b.position[
                                                                          number_b_b[point_a - 1]:number_b_b[
                                                                              point_b - 1]] + sequence_a.position[
                                                                                              number_a_a[
                                                                                                  point_b - 1]:
                                                                                              number_a_a[
                                                                                                  the_number1 - 1]]
    new_breed.size = sequence_a.size[0:number_a_a[point_a - 1]] + sequence_b.size[
                                                                  number_b_b[point_a - 1]:number_b_b[
                                                                      point_b - 1]] + sequence_a.size[
                                                                                      number_a_a[point_b - 1]:
                                                                                      number_a_a[the_number1 - 1]]
    k=0
    for i in range(0,len(new_breed.gif_num)):
       k=k+new_breed.gif_num[i]
    # if len(new_breed.path)!=k:
    #     print("wrong!!!!!!")
    #
    #     print(sequence_a.gif_num[0:point_a])
    #     print(sequence_b.gif_num[point_a:point_b])
    #     print(sequence_a.gif_num[point_b:the_number1])
    #
    #     print(number_a_a)
    #     print(number_b_b)
    #     print(sequence_a.path[0:number_a_a[point_a - 1]])
    #     print(sequence_b.path[number_b_b[point_a - 1]:number_b_b[point_b - 1]])
    #     print(sequence_a.path[number_a_a[point_b - 1]:number_a_a[the_number - 1]])
    #
    #
    #     print(point_b)
    #     print(point_a)
    #     print(sequence_b.gif_num)
    #     print(sequence_a.gif_num)
    #     print(new_breed.gif_num)
    #
    #     print(new_breed.path)
    #     print("..........................")
    return new_breed


def cmp(ak,bk):
    if ak.scores<bk.scores:
        return -1
    else:
        return 1


#主函数 调用函数
def gene_gif_main(path_1,path_2,number,pathhh,weatherrr,colorrr):

    print("遗传算法开始")
    #获取template的选择
    t=get_tempalte.gene_gif_main(number,pathhh,weatherrr,colorrr)

    #加载图片数据 ##等待文件格式
    #pictures
    ###正经程序写在这儿。。
#    data_picture=xlrd.open_workbook(path_2)
#    table_picture=data_picture.sheet_by_name("Sheet1")
#    for i in range(1,number+1):
#        _picture=picture()
##测试输入
    for i in range(0,number):
        pictures.append(picture(colorrr[i],[],weatherrr[i],pathhh[i]))

    #加载所有的gif数据
    data_gif=xlrd.open_workbook(path_1)
    table_gif=data_gif.sheet_by_name("Sheet1")

    gif_numbers=table_gif.nrows
    for i in range(1,gif_numbers):
        strs=table_gif.cell(i,1).value
        factor=strs.split(';')
        
        #_paths=pt+str(table_gif.cell(i,0).value)+".gif"
        #不知道为啥要取一次整数
        aka=round(table_gif.cell(i,0).value)
        _paths = pt + str(aka) + ".gif"
        #_paths=table_gif.cell(i,0).value
        _thecolor=[table_gif.cell(i,2).value,table_gif.cell(i,3).value,table_gif.cell(i,4).value]
        _gif=one_giftem(table_gif.cell(i,0).value,strs,table_gif.cell(i,8).value,[table_gif.cell(i,6).value,table_gif.cell(i,7).value],_paths,_thecolor,table_gif.cell(i,5).value)

        all_gif.append(_gif)
    #先代目和二代目
    pre_gif=[]
    new_gif=[]
    #两代的得分 注意收敛的条件不是得分多低而是两代得分差距不大，认为是无法更优化
    pre_score=0
    new_score=0
    score=0
    #随机生成初代目
    for i in range(0,firsit_num):
        a_gif_Template=gif_Template(number,1,t.no)
        pre_gif.append(a_gif_Template)

    deida_times=0
    while deida_times < ctrl_times:

        #print("il")
        #print(pre_gif)
        new_gif.clear()
        #print("ki")
        #print(pre_gif)
        for i in range(0,len(pre_gif)):
            pre_gif[i].scores=pre_gif[i].gif_fit()

        pre_gif=sorted(pre_gif,key=functools.cmp_to_key(cmp))

        #pre_gif=sorted(pre_gif,key=lambda x:x['scores'])
        #pre_gif.sort()

        for i in range(0,select_num):
            #print(i)
            new_gif.append(pre_gif[i])


        #new

        for the_gif_Template in new_gif:
            #基因突变
            mutation_t=random.randint(0,Gene_mutation_t)
            if mutation_t<Gene_mutation_i:
                the_gif_Template.Gene_mutation()

            # 交叉产生新的个体：
        for i in range(0, firsit_num - select_num):
            mother = random.randint(0, select_num - 1)
            father = random.randint(0, select_num - 1)
            # print(mother)
            # print(father)
            #print("hee")

            new_gif.append(Gene_breed(new_gif[mother], new_gif[father]))
            new_gif[len(new_gif) - 1].scores = new_gif[len(new_gif) - 1].gif_fit()
            #print(new_gif[len(new_gif)-1].gif_num)
            #print(new_gif[len(new_gif) - 1].template)
            #print(new_gif[len(new_gif)-1].scores)


        pre_gif=new_gif[:]
        deida_times=deida_times+1
        # print("soc")
        # print(new_gif[0].scores)
       # for k in range(0,30):
        #    print(new_gif[k].scores)

    return new_gif[0]


def geneticMain(img_num,path,weather,color,factors,load_dict,res_poem):
    #print("img_num: ",img_num)
    kiss=gene_gif_main(xls_file,"",img_num,path,weather,color)
    # print(kiss.gif_num)
    # print(kiss.path)
    # print(kiss.color)
    # print(kiss.template)
    openning = {
        'id' : random.randint(0,len(openning_templates)-1),
        'title' : load_dict["title"],
        'desc' : load_dict["description"],
        'bg_image' : randImage()
    }
    ending = {
        'id' :random.randint(0,len(ending_templates)-1),
        'text' : 'END'
    }
    middle = {
        'num' : len(kiss.template) ,  #模板数目
        'templates': []
    }
    img_cnt = 0
    gif_cnt = 0
    # print(kiss.gif_num)
    for i in range(len(kiss.template)):
        template = {   #模板
            'id' : kiss.template[i],
            'bg_image' : randImage(),
            'images' : path[img_cnt:],
            'gif_num' : kiss.gif_num[i],
            'gifs' : []
        }
        img_cnt = img_cnt + total_photo_template[kiss.template[i]]
        for j in range(kiss.gif_num[i]):
            template['gifs']
            gif_i = {
                'path' : kiss.path[gif_cnt],
                'size' : kiss.size[gif_cnt],
                'position' : kiss.position[gif_cnt],
            }
            template['gifs'].append(gif_i)
            gif_cnt = gif_cnt + 1
        middle['templates'].append(template)

    poem = {
        'num' : 1,
        'templates' : [
            {
                'id' : random.randint(0,len(photo_with_poem_templates)-1),
                'images' : path,
                'poem' : res_poem
            }
        ]
    }
        
    command = {
        'openning': openning,
        'middle': middle,
        'ending': ending,
        'music': randMusic(),
        'poem' : poem,
        'location': './demo.mp4',
        'fps': 5
    }

    return command
    generate.generateMovie(command)



