from .templates import *

def get_long_picture(_template,_gif_num,_gif_path,_pic_path):
    _gif_no=0
    pics=[]
    for i in range(0,len(_pic_path)):
        pic_imgs=Image.open(_pic_path)
        for j in range(0,_gif_num):
            pic_imgs=add_pic(pic_imgs,_gif_path[_gif_no])
            _gif_no=_gif_no+1

        pics.append(pic_imgs)
    return add_pic(_template,pics )

