import random
import os

res_path = "./movie/modules/assets/"
tmp_path = "./tmp/"

font_path = res_path+"fonts/"
images_path = res_path+"images/"
clips_path = res_path+"clips/"
music_path = res_path+"music/"

title_font = ["Kai.ttf","Kose.ttf","Kuaile.ttf","Manhei.ttf",'Wenkai.ttf','Wenyi.otf',"Yozai.ttf","Zhushi.ttf"]
poem_font = ["Kai.ttf","Kose.ttf","Wenkai.ttf","Yozai.ttf","Zhushi.ttf"]
default_images = os.listdir(images_path+"default/")
rainy_images = os.listdir(images_path+"rainy/")
sunny_images = os.listdir(images_path+"sunny/")
winter_images = os.listdir(images_path+"winter/")
poem_images = os.listdir(images_path+"poem/")

music = ["1.mp3","2.mp3","3.mp3"]

bg_video = {
    'rainy' : ['rainy1.mp4', 'rainy2.mp4','water1.mp4' ],
    'snow': ['snow1.mp4','snow2.mp4'],
    'sunny': ['sunny1.mp4', 'sunny2.mp4'],
    'default' : ['water1.mp4', 'sunny1.mp4']
}

def get_bg_video(tag):
    if tag in bg_video:
        return clips_path+random.sample(bg_video[tag],1)[0]
    return clips_path+random.sample(bg_video['default'],1)[0]

def randFont():
    return font_path+random.sample(title_font,1)[0]

def randPoemFont():
    return font_path+random.sample(poem_font,1)[0]

def randPoemBg():
    return images_path+"poem/"+random.sample(poem_images,1)[0]

def randImage():
    return images_path+"default/"+random.sample(default_images,1)[0]
def randRainy():
    return images_path+"rainy/"+random.sample(rainy_images,1)[0]
def randSunny():
    return images_path+"sunny/"+random.sample(sunny_images,1)[0]
def randWinter():
    return images_path+"winter/"+random.sample(winter_images,1)[0]

def randMusic():
    return music_path+random.sample(music,1)[0]


