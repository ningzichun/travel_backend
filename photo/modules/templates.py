from PIL import Image
import random
#定义模板类
class template:
    def __init__(self,_angle,_number,_position,_path,_size):
        self.angle=_angle
        self.position=_position
        self.size=_size
        self.number=_number
        self.path=_path
#为图片贴gif
def add_gif(_img,gif_path):
    img=Image.open(gif_path)
    img=img.convert('RGBA')
    img = img.convert('RGBA')
    r, g, b, a = img.split()

    _img.paste(img,(0,0),mask=1)#加前景
    return _img
#为模板贴图片
def add_pic(_template,pics): #输入参数： 位置信息，图片数量，旋转角度
    its=Image.open("_template.path")
    for i in range(0,len(pics)):
        img=pics[i].convert("RGBA")
        img=img.rotate(_template.angle[i],expand=1)
        r,g,b,a=img.split()
        its.paste(img,(_template.position[i][0],_template.position[i][1]),mask=1)

    return its

