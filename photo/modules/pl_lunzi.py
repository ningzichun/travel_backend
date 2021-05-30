#pil 一些自产的轮子
from PIL import Image, ImageDraw, ImageFont
import cv2
import xlrd
import os
import random
mask_num=0.1
import numpy as np
from . import get_template as gt

pt2="./photo/modules/resources/3/"
class fanhui:
    def __init__(self,_positions,_img):
        self.position=_positions
        self._img=_img
#带
def get_ok(src,pre,w,h,wp,hp):
    if src < w*h*mask_num:
        for i in range(len(pre)):
            if max(wp,pre[i][0])>min(w+wp,pre[i][1]):
                p=1
            elif min(pre[i][3],h+hp)<max(h,pre[i][2]):
                p=1
            else:
                return 0
        return 1
    else:
        return 0
#带显著性检测的贴图
def add_gif(_img,gif_path,no,pre,tap,test_root):
    k=150
    real_path = pt2 + str(gif_path) + ".png"
    src = Image.open(real_path)
    src1=src
    img=_img
    p_positon=[]
    numsrc = cv2.imread(test_root+str(no)+'linshi.png')
    numsrc = cv2.cvtColor(numsrc, cv2.COLOR_BGR2GRAY)  # 灰度化处理
    numsrc = cv2.threshold(numsrc, 127, 1, cv2.THRESH_BINARY)
    #os.remove(str(no)+'linshi.png')
    times = 4  # 缩小的倍数
    ok = 0
    position = []
    ks = int(img.width / k) #
    for i in range(4, 7):
        w_ks = int(int(img.width / ks) / i)  # 原图缩小五倍宽的尺寸
        h_ks = int(int(img.height / ks) / i)  # 原图
        w_ds = int(src.width / w_ks)  # 前景图放大的倍数
        h_ds = int(src.height / h_ks)
        ds = max(w_ds, h_ds)
        # print(gif_path)
        # print(w_ds)
        # print(h_ds)
        # print(int(src.width / ds))
        # print(int(src.height / ds))
        src = src.resize((int(src.width / ds), int(src.height / ds)))  # 新的（合适尺寸）前景图

        ok = 0
        # print(numsrc)
        for j in range(100):
            w_position = random.randint(0, int(img.width / ks) - src.width)
            if tap==1:#底部元素
                h_position = random.randint(int((int(img.height / ks) - src.height)*4/5), int(img.height / ks) - src.height)
            elif tap==2:#顶部元素
                h_position = random.randint(0,int((int(img.height / ks) - src.height)*1/4))
            else:
                h_position = random.randint(0, int(img.height / ks) - src.height)
            kl = 0
            for p1 in range(0, src.width):
                for p2 in range(0, src.height):
                    kl = kl + int(numsrc[1][p1][p2])
            # print("//////////////////////////////////////")
            # print(w_position)
            # print(h_position)
            # print(kl)
            # print(src.width)
            # print(src.height)
            # print(mask_num)
            # print("//////////////////////////////////////")
            ts=get_ok(kl,pre,src.width,src.height,w_position,h_position)
            if ts == 1:
                ok = 1
                times = i
                position = [w_position, h_position]
                p_positon=[w_position,w_position+src.width,h_position,h_position+src.height]
                break
        if ok == 1:
            break
    if ok == 1:  # 贴图部分的代码

        w_ks = int(int(img.width / ks) / times)  # 原图缩小五倍宽的尺寸
        h_ks = int(int(img.height / ks) / times)  # 原图
        w_ds = int(src1.width / w_ks)  # 前景图放大的倍数
        h_ds = int(src1.height / h_ks)
        ds = max(w_ds, h_ds)
        src = src1.resize((int((src1.width / ds) * ks), int((src1.height / ds) * ks)))  # 新的（合适尺寸）前景图

        src.convert("RGBA")
        r, g, b, a = src.split()
        # print(int((src1.width / ds) * ks))
        # print(int((src1.height / ds) * ks))
        # print(int(position[0] * ks))
        # print(int(position[1] * ks))
        img.paste(src, (int(position[0] * ks), int(position[1] * ks)), mask=a)
    return img,p_positon

#任意位置加字体，（参数：图像，路径，颜色，字号，内容
def add_text(image,path,color,size,text,position):
    font = ImageFont.truetype(path, size)
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    print(rgba_image)
    #text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)
    # 设置文本颜色和透明度
    image_draw.text((position[0],position[1]), text, font=font, fill=(color[0],color[1],color[2],color[3]))

    image_with_text = Image.alpha_composite(rgba_image, text_overlay)

    return image_with_text


#任意图片贴一张照片 不加显著性检测
def add_pic(backgroud,pic,position):
    back = backgroud
    back.resize((backgroud.width, backgroud.height))
    its = backgroud
    its.convert("RGBA")
    r, g, b, a = its.split()
    img = pic
    w = img.width
    h = img.height

    ws = position[2]-position[0]
    hs = position[3]-position[1]
    wls = min(w / ws, h / hs)

    img = img.resize((int(w / wls), int(h / wls)))
    w1 = img.width
    h1 = img.height
    box = ((w1 - ws) / 2, (h1 - hs) / 2, w1 - (w1 - ws) / 2, h1 - (h1 - hs) / 2)  #
    img = img.crop(box)

    back.paste(img, (position[0], position[1]))
    back.paste(its, (0, 0), mask=a)
    return back


#显著性检测的box
def get_box(src,height,weight):
    # src=[[0 ,0 ,0 ,0 ,0, 0, 0],
    #      [0, 0, 1, 0, 0, 0, 0],
    #      [0, 0, 1, 0, 0, 0, 0],
    #      [0, 0, 1, 1, 0, 1, 0],
    #      [0, 0, 0, 1, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0],
    #      ]
    # weight=7

   # dst = cv2.adaptiveThreshold(src, 102, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 1)#二值化
    #print(src[1])
    ok = 0
    tx = 0
    up = 0
    down = height
    left = 0
    right = weight

    # 找到矩形的left 和 right
    #
    # print(src)
    # 找到矩形up和down：
    for i in range(height):
        pre_tx = tx
        tx = 0
        for j in range(weight):
            tx = tx + src[1][i][j]
        if i!=1:
            if up==0 and pre_tx == 0 and tx != 0:
                up = i
            elif down==height and pre_tx != 0 and tx == 0:
                down = i
    # 找到矩形的left 和 right

    tx = 0
    for i in range(weight):
        pre_tx = tx
        tx = 0
        for j in range(height):
            tx = tx + src[1][j][i]
        if i != 1:
            if left==0 and pre_tx == 0 and tx != 0:
                left = i
            elif right==weight and pre_tx != 0 and tx == 0:
                right = i



    box=[up,down,left,right]
    return box
#带显著性检测的 贴图获取位置
def getposition(img,box,weight,height):

    w=img.width
    h=img.height
    # w=150
    # h=400
    h_middle=(box[0]+box[1])/2

    w_middle=(box[2]+box[3])/2
    h_middle=200
    w_middle=150
    wls=w/weight
    hls=h/height
    # print(wls)
    # print(hls)
    if wls>hls:
        # print("1")
        w2=weight*hls
        # print(w2)
        h2=height*hls
        # print(hls)
        left=0
        right=0
        up =0
        down=h2
        if w_middle < w2/2:
            left=0
            right=w2
        elif w_middle > w-w2/2:
            left=w-w2
            right=w
        else:
            left=w_middle-w2/2
            right=w_middle+w2/2
        box=[up/hls,down/hls,left/hls,right/hls,hls]
        return box
    else:

        w2=weight*wls
        h2=height*wls
        up=0
        down=0
        left=0
        right=w2
        # print("right")
        # print(right)
        if h_middle < h2 / 2:
            up = 0
            down = h2
        elif h_middle > h-h2/2:
            up = h - h2
            down = h
        else:
            up = h_middle - h2 / 2
            down = h_middle + h2 / 2
        box = [up / wls, down / wls, left / wls, right / wls,wls]
        return box


def get_main_pics(img,weight,height,num,test_root):
    k=img.width/150
    img1=img.resize((int(img.width/k),int(img.height/k)))
    src = cv2.imread(test_root+str(num)+ 'linshi.png')
    height1=src.shape[0]
    wieght1=src.shape[1]
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  # 灰度化处理
    src = cv2.threshold(src, 127, 1, cv2.THRESH_BINARY)
    box=get_box(src,height1,wieght1)
    box1=getposition(img,box,weight,height)
    w1=img.width
    h1=img.height
    # print(box1)
    # print(int(w1/box1[4]))
    # print(int(h1/box1[4]))

    img=img.resize((int(w1/box1[4]),int(h1/box1[4])))
    box3=[box1[2],box1[0],box1[3],box1[1]]
    img=img.crop(box3)
    # print(box1)
    return img
