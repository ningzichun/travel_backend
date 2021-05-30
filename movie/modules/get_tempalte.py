# 遗传算法，为最后一层生成参数
# 输出：
# 第一个参数这个影集照片数量，第二个参数是一个数组 第i项代表第i张图片的gif数量，第三个参数是一个数组，第i项是第i个gif 的id（现在是地址），(第四个参数是规定尺寸
# 第五个参数是规定位置，这个可以根据id一起取？最后再说吧，不行就三个参数是地址 尺寸位置)最后一个参数是音乐的卡点时间

# 输入数据格式：
import random
from . import cost_calculate11 as cc
import xlrd
import functools
import copy

from . import templates as tems 

pt = "./movie/modules/assets/gifs/"  # 资源文件目录
xls_file = r"./movie/modules/assets/gifs/info.xls"  # xls文件

# 加载图片类
class picture:
    def __init__(self, _color, _factor, _weather, _path):
        picture.color = _color
        picture.factor = _factor
        picture.path = _path
        picture.weather = _weather

def pic_lodain(picture_number):
    photos = []
    photo = picture()

# tem数据库装入缓存的定义
class one_tem:
    def __init__(self, _id, _factor, _num, _color, _weather):
        self.id = _id
        self.factor = _factor
        self.num = _num #容纳照片的数量
        self.color = _color
        self.weather = _weather

# 全局变量  和  参数定义：
pictures = []
# apicture=picture()
# pictures.append(apicture)#加载入图片类

k = 10  # 模板的数量
p_allgif_t = 10
p_allgif_i = 3  # p_allgif_i / p_allgif_t gif的产生率 对于初代而言
all_tem = []  # gif表装入内存
# a=one_giftem()
# all_gif.append(a)

Gene_mutation_t = 1000
Gene_mutation_i = 200
# 变异率 Gene_mutation_i / Gene_mutation_t
Gene_mutation_no = 3  # 最大的变异点位数

#
firsit_num = 50  # 初代目的数量
select_num = 20
theta_score = 10  # 收敛阈值

# 最大的迭代次数
ctrl_times = 100

# 模板类的定义
# 模板类的定义
class gif_Template:
    # 构造函数用于生成初代：
    def __init__(self, photo_num, ini):
        self.pic_num = photo_num  # 图片数量
        self.num = []  # gif数量（数组）  新版本是针对模板来
        self.no = []  # 路径
        self.color = []
        self.weather = []
        self.factor = []
        self.scores = 0
        # 提示要初始化的时候才进行
        if ini != 0:
            left_picture = self.pic_num
            # 先把模板的数量给匹配出来
            while left_picture != 0:
                ok = 1
                while ok == 1:

                    rand_template_no = random.randint(0, len(all_tem) - 1)
                    if all_tem[rand_template_no].num <= left_picture:
                        ok = 0
                self.num.append(all_tem[rand_template_no].num)
                self.color.append(all_tem[rand_template_no].color)
                self.factor.append(all_tem[rand_template_no].factor)
                self.weather.append(all_tem[rand_template_no].weather)
                self.scores=0
                self.no.append(all_tem[rand_template_no].id)
                left_picture = left_picture - all_tem[rand_template_no].num
            # 给每个模板挨个匹配gif

        # ...用于不同位置的模板这里还可以加

    # 变异
    # 编码方式：整数编码
    def Gene_mutation(self):
        p_mutation = random.randint(0, Gene_mutation_t)
        if p_mutation < Gene_mutation_i:  # 变异概率
            times = random.randint(0, Gene_mutation_no)  # 变异的点位数
            for i in range(0, times):
                point_no = len(self.no)
                if point_no != 0:
                    point = random.randint(0, point_no-1)
                    ok=1
                    max_times=1000
                    ttime=0
                    while ok==1 and ttime<max_times:
                        mutation_point = random.randint(0, k)
                        # print(mutation_point)
                        # print(all_tem[0].num)
                        # print(self.num[point])
                        if all_tem[mutation_point].num==self.num[point]:
                            ok=0
                        ttime=ttime+1
                    if ok==0:
                        self.no[point] = all_tem[mutation_point].id
                        self.color[point] = all_tem[mutation_point].color
                        self.factor[point] = all_tem[mutation_point].factor
                        self.weather[point] = all_tem[mutation_point].weather

    # 适应性函数
    def tem_fit(self):
        number = len(self.no)#模板数量号
        cost = 0
        gif_no = 0  # gif编号
        pic_no = 0  # picture编号
        # print(self.gif_num)
        # print(number)
        # print(self.template)i
        for i in range(0, number):
            for y in range(0, self.num[i]):
                cost = cost + cc.color_weight * cc.color(pictures[pic_no].color, self.color[i])
                cost = cost + cc.factor_weight * cc.factor(pictures[pic_no].factor, self.factor[i])
                cost = cost + cc.weather_weight * cc.weather(pictures[pic_no].weather, self.weather[i])
                cost = cost + cc.chongfu2(self)
                # print("cost")
                # print(cost)
                pic_no = pic_no + 1
        return cost

    def __lt__(self, other):
        return self.scores < other.scores


# 交叉产生下一代
# 重写函数：
def Gene_breed(sequence_a, sequence_b):
    # print("begin")
    if len(sequence_a.no) == 1:
        return sequence_b
    if len(sequence_b.no) == 1:
        return sequence_a

    new_breed = gif_Template(sequence_a.pic_num, 0)

    the_number1 = len(sequence_a.no)
    the_number = min(len(sequence_a.no), len(sequence_b.no))

    _point_a = random.randint(1, the_number - 1)
    _point_b = random.randint(1, the_number - 1)
    point_a = min(_point_a, _point_b)
    point_b = max(_point_a, _point_b)

    #继承父还是母亲的基因
    rank=0

    _from=0
    begin=0
    num=0
    left_picture=sequence_a.pic_num
    if left_picture<0:
        a=[]
        # print(a[5])
    # print("1")
    # print(left_picture)
    begin_nos=0
    while left_picture != 0:
        #print("1")
        #rand阶段
        if rank:
            ok=0
            while ok==0:
                
                rand_template_no = random.randint(0, len(all_tem) - 1)
                if left_picture<0:
                    a=[]
                    # print(a[5])
                # print(rand_template_no)
                # print(all_tem[rand_template_no].num)
                #
                # print(left_picture)
                # print("pppppppppppppppppppp")
                if all_tem[rand_template_no].num <= left_picture:
                    ok = 1
            new_breed.num.append(all_tem[rand_template_no].num)
            new_breed.color.append(all_tem[rand_template_no].color)
            new_breed.factor.append(all_tem[rand_template_no].factor)
            new_breed.weather.append(all_tem[rand_template_no].weather)
            new_breed.no.append(all_tem[rand_template_no].id)
            left_picture = left_picture - all_tem[rand_template_no].num
            if left_picture<0:
                a=[]
                # print(a[5])
           # print("1")
            # print(left_picture)
            continue
        if begin>point_a:
            _from=1
        if begin>point_b:
            _from=0
        if begin>=min(len(sequence_a.no)-1,len(sequence_a.no)-1):
            rank=1
            continue
        
        if _from==0:
            aka=sequence_a.num[begin]
            if(aka>left_picture):
                rank=1
                continue
            new_breed.num.append(all_tem[sequence_a.no[begin]].num)
            new_breed.color.append(all_tem[sequence_a.no[begin]].color)
            new_breed.factor.append(all_tem[sequence_a.no[begin]].factor)
            new_breed.weather.append(all_tem[sequence_a.no[begin]].weather)
            new_breed.no.append(all_tem[sequence_a.no[begin]].id)
            left_picture = left_picture - all_tem[sequence_a.no[begin]].num
            if left_picture<0:
                a=[]
                # print(a[5])
            # print("1")
            # print(left_picture)
        else:
            aka = sequence_b.num[begin]
            if (aka > left_picture):
                rank = 1
                continue
            new_breed.num.append(all_tem[sequence_b.no[begin]].num)
            new_breed.color.append(all_tem[sequence_b.no[begin]].color)
            new_breed.factor.append(all_tem[sequence_b.no[begin]].factor)
            new_breed.weather.append(all_tem[sequence_b.no[begin]].weather)
            new_breed.no.append(all_tem[sequence_b.no[begin]].id)
            left_picture = left_picture - all_tem[sequence_b.no[begin]].num
            if left_picture<0:
                a=[]
                # print(a[5])
            # print("1")
            # print(left_picture)
        begin=begin+1
    # print("end")
    return new_breed


def cmp(ak, bk):
    if ak.scores < bk.scores:
        return -1
    else:
        return 1


# 主函数 调用函数 获得模板
def gene_gif_main(number, pathhh, weatherrr, colorrr):
    # 加载图片数据
    # pictures
    ###程序入口
    #    data_picture=xlrd.open_workbook(path_2)
    #    table_picture=data_picture.sheet_by_name("Sheet1")
    #    for i in range(1,number+1):
    #        _picture=picture()
    ##测试输入
    for i in range(0, number):
        pictures.append(picture(colorrr[i], [], weatherrr[i], pathhh[i]))

    # 加载所有的tem数据
    for i in range(len(tems.total_photo_template)):
        _tem = one_tem(i,"",tems.total_photo_template[i],tems.photo_templates_color[i],tems.photo_templates_weather[i])
        all_tem.append(_tem)
    # 先代目和二代目
    pre_tem = []
    new_tem = []
    # 两代的得分 注意收敛的条件不是得分多低而是两代得分差距不大，认为是无法更优化
    pre_score = 0
    new_score = 0
    score = 0
    # 随机生成初代目
    print("遗传算法生成初代")
    for i in range(0, firsit_num):
        a_gif_Template = gif_Template(number, 1)
        pre_tem.append(a_gif_Template)
    deida_times = 0
    print("遗传算法进行中")
    while deida_times < ctrl_times:
        new_tem.clear()
        for i in range(0, len(pre_tem)):
            pre_tem[i].scores = pre_tem[i].tem_fit()

        pre_tem = sorted(pre_tem, key=functools.cmp_to_key(cmp))
        for i in range(0, select_num):
            # print(i)
            new_tem.append(pre_tem[i])

        # new

        for the_gif_Template in new_tem:
            # print(deida_times)
            # 基因突变
           # mutation_t = random.randint(0, Gene_mutation_t)
           # if mutation_t < Gene_mutation_i:
            the_gif_Template.Gene_mutation()

            # 交叉产生新的个体：
        # print("lllllll")
        for i in range(0, firsit_num - select_num):
            # print("LLLL")
            mother = random.randint(0, select_num - 1)
            father = random.randint(0, select_num - 1)

            new_tem.append(Gene_breed(new_tem[mother], new_tem[father]))
            new_tem[len(new_tem) - 1].scores = new_tem[len(new_tem) - 1].tem_fit()

        pre_tem = new_tem[:]
        deida_times = deida_times + 1
        # print("soc")
        # print(new_tem[0].scores)
    # for k in range(0,30):
    #    print(new_tem[k].scores)
    print("遗传算法完成")
    return new_tem[0]


# t=gene_gif_main(7,[0,1,2,3,4,5,6],[1,1,1,1,1,1,1],[[100,100,100],[100,100,100],[100,100,100],[100,100,100],[100,100,100],[100,100,100],[100,100,100]])
# print(t.color)
# print(t.no)
# print(t.num)
# print(t.weather)
