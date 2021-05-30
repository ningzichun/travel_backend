from PIL import Image, ImageDraw, ImageFont
import cv2
import caijian_main as cm
import lunzi as lz
import os
#参数格式：
def get_main_pics(path,name,weight,height):
    img=Image.open(path+name)
    k=img.width/150
    img1=img.resize((int(img.width/k),int(img.height/k)))
    img1.save(path+"linshi.jpg")
    src=cm.get_cv(path,"linshi.jpg")
    box=lz.get_box(src)
    os.remove(path+"linshi.jpg")
    box1=lz.getposition(img,box,weight,height)
    w1=img.width
    h1=img.height
    print(box1)
    print(int(w1/box1[4]))
    print(int(h1/box1[4]))

    img=img.resize((int(w1/box1[4]),int(h1/box1[4])))
    box3=[box1[2],box1[0],box1[3],box1[1]]
    img=img.crop(box3)
    print(box1)
    return img

