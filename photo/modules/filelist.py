import random
import os

res_path = "./movie/modules/assets/"
tmp_path = "./tmp/"

font_path = res_path+"fonts/"
images_path = res_path+"images/"
music_path = res_path+"music/"
masks_path = res_path+"masks/"

title_font = ["CEYY.ttf","Seto.ttf","Xiyue.ttf","ZHUSHI.ttf"]
poem_font = ["STXINGKA.TTF","STXINWEI.TTF"]
images = os.listdir(images_path)

def randFont():
    return font_path+random.sample(title_font,1)[0]

def randPoemFont():
    return font_path+random.sample(poem_font,1)[0]

def randImage():
    return images_path+random.sample(images,1)[0]