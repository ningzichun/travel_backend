from PIL import Image
import xlrd
import random
import numpy as np
#定义模板类
import math

template_xls = "./photo/modules/templates/template.xls"
tmp_path = "./photo/modules/templates/"
class template:
    def __init__(self,_angle,_position,_path,_all,_color,_weather,_factor):
        self.all=_all
        self.angle=_angle
        self.position=_position
        self.path=_path
        self.color=_color
        self.weather=_weather
        self.factor=_factor
#为图片贴gif
def add_gif(_img,gif_path):
    img=Image.open(gif_path)
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

def add_pic(_template,pics,mark):
    print(">")
    print(_template)
    tos=mark%(_template.all)
    tos=int(tos)
    print("hi")
    print(_template.path)
    print(_template.path[tos])
    real_path=tmp_path+_template.path[tos]
    its=Image.open(real_path)
    its.convert("RGBA")
    r, g, b, a = its.split()
    img=pics[mark]
    w = img.width
    h = img.height

    ws=int(_template.position[tos][2])-int(_template.position[tos][0])
    hs=int(_template.position[tos][3])-int(_template.position[tos][1])
    wls=min(w/ws,h/hs)

    img=img.resize((int(w/wls),int(h/wls)))
    w1=img.width
    h1=img.height
    box = ((w1 - ws) / 2, (h1 - hs) / 2, w1 - (w1 - ws) / 2, h1 - (h1 - hs) / 2)  #
    img = img.crop(box)

    img=img.rotate(int(_template.angle[tos]),expand=1)
    its.paste(img,(int(_template.position[tos][0]),int(_template.position[tos][1])))
    return its
#拼接图片
def split_picture(_template,pics):
    begin=0
    im=[]
    for i in range(0,len(pics)):
        imgs=add_pic(_template,pics,i)
        print("?")
        if begin==0:
            im=np.array(imgs)
            begin=1
        else:
            km=np.array(imgs)
            im=np.concatenate((im, km), axis = 0)
            c=Image.fromarray(im)
            #c.show()
    return Image.fromarray(im)
def get_long_picture(_template,_gif_num,_gif_path,_pic_path,cover_path):
    _gif_no=0
    pics=[]
    cover_got = 0
    cover_height = 0
    cover_width = 0
    for i in range(0,len(_pic_path)):
        print(_pic_path)
        pic_imgs=Image.open(_pic_path[i])
        for j in range(0,_gif_num[i]):
            pic_imgs=add_gif(pic_imgs,_gif_path[_gif_no])
            _gif_no=_gif_no+1
        if not cover_got:   #封面生成
            pic_imgs.save(cover_path)
            cover_height = pic_imgs.height
            cover_width = pic_imgs.width
            cover_got = 1
        pics.append(pic_imgs)
    return split_picture(_template,pics),cover_width,cover_height
all_template=[]

def load_template(paths):
    print(">")
    data_template=xlrd.open_workbook(paths)
    table_template=data_template.sheet_by_name("Sheet1")
    num=table_template.nrows
    for i in range(1,num):
        print(i)
        angle=table_template.cell(i,1).value
        angle=angle.split(",")
        num=table_template.cell(i,2).value
        positions=table_template.cell(i,3).value
        print("llll")
        print(positions)
        positions=positions.split("/")
        print("ppp")
        print(positions)
        position1=positions[0].split(",")
        position2=positions[1].split(",")
        position=[position1,position2]
        pathes=table_template.cell(i,4).value
        pathes=pathes.split(",")
        color=table_template.cell(i,5).value
        print(color)
        color=color.split("/")
        weather = table_template.cell(i, 6).value
        factor = table_template.cell(i, 7).value

        _template=template(angle,position,pathes,num,color,weather,factor)

        all_template.append(_template)



# 测试
#a1=template([0,0],0,[[79,213,983,955],[272,39,966,827]],["2.png","1.png"],[0,0],2,[255,255,255],4,[])
#a2=template([0,0],0,[[0,179,781,1215],[299,103,911,904]],["2_1.png","2_2.png"],[0,0],2,[244,255,236],3,[])
#a3=template([0,0],0,[[112,56,1036,751],[0,29,1154,899]],["3_1.png","3_2.png"],[0,0],2,[242,228,97],3,[])

def get_best_template(colors,weathers,factors):
    print("I/,m Here")
    load_template(template_xls)
    print(all_template[0].color)
    num=0
    score=-100000000
    for i in range(0,len(all_template)):
        _score=math.sqrt((int(all_template[i].color[0])-colors[0])*(int(all_template[i].color[0])-colors[0])+(int(all_template[i].color[0])-colors[1])*(int(all_template[i].color[0])-colors[1])+(int(all_template[i].color[0])-colors[2])*(int(all_template[i].color[0])-colors[2]))
        #_score = math.sqrt((all_template[i].color[0] - colors[0]) * (all_template[i].color[0] - colors[0]) + (
#                    all_template[i].color[0] - colors[1]) * (all_template[i].color[0] - colors[1]) + (
 #                                      all_template[i].color[0] - colors[2]) * (
  #                                     all_template[i].color[0] - colors[2]))
        print(all_template[i].weather)
        if int(all_template[i].weather) == weathers:
            _score=_score-100
        else:
            # print("weather")
            # print((weather_a-weather_b)*(weather_a-weather_b))
            _score=_score+(int(all_template[i].weather) - weathers) * (int(all_template[i].weather) - weathers)

        if score>_score:
            num=i
    print("lllllllllllllllllll")
    print(all_template[0])
    print(all_template[1])
    print(all_template[2])

    print(num)
    return all_template[num]


