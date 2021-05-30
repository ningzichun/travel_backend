from PIL import Image
import xlrd
import random
import numpy as np
from . import get_template as gt
from . import pl_lunzi as pl
from . import begin_plog as bp
import sys
import importlib
importlib.reload(sys)
#定义模板类
import math
pt1="./photo/modules/resources/1/"
pt2="./photo/modules/resources/2/"
pt = "./photo/modules/templates/"
template_xls = "./photo/modules/templates/template.xls"
tmp_path = "./photo/modules/templates/"
bg_image = './photo/modules/resources/background.png'
class template:
    def __init__(self,_angle,_position,_path,_all,_color,_weather,_factor,_size):
        self.all=_all
        self.angle=_angle
        self.position=_position
        self.path=_path
        self.color=_color
        self.weather=_weather
        self.factor=_factor
        self.size=_size
#为图片贴gif
def add_gif(_img,gif_path):
    if _img.width>_img.height:
        real_path=pt2+str(gif_path)+".png"
    else:
        real_path=pt1+str(gif_path)+".png"
    img=Image.open(real_path)
    print(gif_path)
    img=img.resize((_img.width,_img.height))
    img = img.convert('RGBA')
    r, g, b, a = img.split()
    #img.show()
    _img.paste(img,(0,0),mask=a)#加前景
    #_img.show()
    return _img
#为模板贴图片
def add_pic1(_template,pics): #输入参数： 位置信息，图片数量，旋转角度
    its=Image.open(_template.path)
    for i in range(0,len(pics)):
        img=pics[i].convert("RGBA")
        img=img.rotate(_template.angle[i],expand=1)
        r,g,b,a=img.split()
        its.paste(img,(_template.position[i][0],_template.position[i][1]),mask=1)

    return its
#在单个模板上，加图片
##v2.0时代的操作手段：底层是白板，第二层是照片，第三层是蒙版
def new_add_pic(_template,pics,tos,test_root):
    tos=int(tos)
    img=pics[tos]
    aka=int(_template.path[tos]) #模板号

    real_path = pt + str(aka) + ".png"
    aka = aka - 1
    backgroud = Image.open(bg_image)  ##更改的地方，写一个绝对路径就好

    backgroud = backgroud.resize((int(gt.all_gif[aka].size[0]), int(gt.all_gif[aka].size[1])))
    its=Image.open(real_path)
    its.convert("RGBA")
    r, g, b, a = its.split()

    ws=int(gt.all_gif[aka].position[2])-int(gt.all_gif[aka].position[0])
    hs=int(gt.all_gif[aka].position[3])-int(gt.all_gif[aka].position[1])
    imgs=pl.get_main_pics(img,ws,hs,tos,test_root)

    backgroud.paste(imgs, (int(gt.all_gif[aka].position[0]), int(gt.all_gif[aka].position[1])))
    backgroud.paste(its, (0, 0), mask=a)
    # its.paste(img,(int(_template.position[tos][0]),int(_template.position[tos][1])))

    return backgroud


def add_pic(_template,pics,tos):
    # print(">")
    #tos=mark%(_template.all)
    tos=int(tos)
    #照片的尺寸
    img = pics[tos]
    w = img.width
    h = img.height
    ws = int(_template.position[tos][2]) - int(_template.position[tos][0])
    hs=int(_template.position[tos][3])-int(_template.position[tos][1])
    #尺寸转换
    #照片 4：3
    if w>h:
        if ws<hs:
            aka=int(_template.path[tos])+2
        else:
            aka=int(_template.path[tos])
    else:
        if ws>hs:
            aka=int(_template.path[tos])-2
        else:
            aka=int(_template.path[tos])
   # gt.all_gif[aka]
    real_path=pt + str(aka) + ".png"
    aka=aka-1
    backgroud=Image.open(bg_image)##更改的地方，写一个绝对路径就好
    # print(_template.size)
    #backgroud=backgroud.resize((int(_template.size[tos][0]),int(_template.size[tos][1])))
    backgroud = backgroud.resize((int(gt.all_gif[aka].size[0]), int(gt.all_gif[aka].size[1])))
    its=Image.open(real_path)
    its.convert("RGBA")
    r, g, b, a = its.split()


    # print(tos)
    # print(_template.position)
    #ws=int(_template.position[tos][2])-int(_template.position[tos][0])
    #hs=int(_template.position[tos][3])-int(_template.position[tos][1])
    ws=int(gt.all_gif[aka].position[2])-int(gt.all_gif[aka].position[0])
    hs=int(gt.all_gif[aka].position[3])-int(gt.all_gif[aka].position[1])
    wls=min(w/ws,h/hs)

    img=img.resize((int(w/wls),int(h/wls)))
    w1=img.width
    h1=img.height
    box = ((w1 - ws) / 2, (h1 - hs) / 2, w1 - (w1 - ws) / 2, h1 - (h1 - hs) / 2)  #
    img = img.crop(box)

    #img=img.rotate(int(_template.angle[tos]),expand=1)
    backgroud.paste(img,(int(gt.all_gif[aka].position[0]),int(gt.all_gif[aka].position[1])))
    backgroud.paste(its,(0,0),mask=a)
   # its.paste(img,(int(_template.position[tos][0]),int(_template.position[tos][1])))

    return backgroud
#拼接图片
def split_picture(_template,pics,test_root,city_image_path,poem):
    print("合成图片中")
    begin=0
    image_begin=bp.get_begin(city_image_path)
    image_begin=image_begin.convert("RGB")
    im=np.array(image_begin)
    for i in range(0,len(pics)):
        imgs=new_add_pic(_template,pics,i,test_root)
        #imgs.save(str(i)+"demo"+".png")
       # imgs.show()
        print("图片"+str(i)+'('+str(imgs.width)+','+str(imgs.height)+')')
        # if begin==0:
        #     im=np.array(imgs)
        #     begin=1
        # else:
        km=np.array(imgs)      #
        im=np.concatenate((im, km), axis = 0)    #
        c=Image.fromarray(im)
           # c.show()
    #释放显著性矩阵文件
    image_end=bp.get_end(poem)
    image_end = image_end.convert("RGB")
    km=np.array(image_end)
    im = np.concatenate((im, km), axis=0)
    return Image.fromarray(im)
def get_long_picture(_template,_gif_tap,_gif_num,_gif_path,_pic_path,cover_path,test_root,city_image_path,poem):
    _gif_no=0
    pics=[]
    cover_got = 0
    cover_height = 0
    cover_width = 0
    for i in range(0,len(_pic_path)):
        pre=[]
        print("生成图片"+str(i))
        pic_imgs=Image.open(_pic_path[i])
        for j in range(0,_gif_num[i]):
            #pic_imgs=add_gif(pic_imgs,_gif_path[_gif_no])
            pic_imgs,pres=pl.add_gif(pic_imgs,_gif_path[_gif_no],i,pre,_gif_tap[_gif_no],test_root)
            _gif_no=_gif_no+1
            if len(pres)!=0:
                pre.append(pres)
        if not cover_got:   #封面生成
            pic_imgs.save(cover_path)
            cover_height = pic_imgs.height
            cover_width = pic_imgs.width
            cover_got = 1
        pics.append(pic_imgs)
    return split_picture(_template,pics,test_root,city_image_path,poem),cover_width,cover_height
all_template=[]

def load_template(paths):
    data_template=xlrd.open_workbook(paths)
    table_template=data_template.sheet_by_name("Sheet1")
    num=table_template.nrows
    for i in range(1,num):

        angle=table_template.cell(i,1).value
        angle=angle.split(",")
        num=table_template.cell(i,2).value
        positions=table_template.cell(i,3).value

        positions=positions.split("/")

        position=[]
        for t in positions:
            position.append(t.split(","))

        pathes=table_template.cell(i,4).value
        pathes=pathes.split(",")
        color=table_template.cell(i,5).value
        color=color.split("/")
        weather = table_template.cell(i, 6).value
        factor = table_template.cell(i, 7).value

        sizes=table_template.cell(i, 8).value
        sizes=sizes.split("/")
        size=[]
        for t in sizes:
            size.append((t.split(",")))
        _template=template(angle,position,pathes,num,color,weather,factor,size)

        all_template.append(_template)



# 测试

def get_best_template(colors,weathers,factors):
    load_template(template_xls)
    num=0
    score=-100000000
    for i in range(0,len(all_template)):
        _score=math.sqrt((int(all_template[i].color[0])-colors[0])*(int(all_template[i].color[0])-colors[0])+(int(all_template[i].color[0])-colors[1])*(int(all_template[i].color[0])-colors[1])+(int(all_template[i].color[0])-colors[2])*(int(all_template[i].color[0])-colors[2]))
        if int(all_template[i].weather) == weathers:
            _score=_score-100
        else:
            # print("weather")
            # print((weather_a-weather_b)*(weather_a-weather_b))
            _score=_score+(int(all_template[i].weather) - weathers) * (int(all_template[i].weather) - weathers)

        if score>_score:
            num=i

    return all_template[4]


