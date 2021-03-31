import os
from PIL import Image, ImageFilter, ImageEnhance
from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects
import numpy as np
import time
from random import randint

screensize = (1920, 1080)
crossTime = 1
res_path = "./travel/resources/assets/"
tmp_path = "./tmp/"
default_font = res_path+"zhenghei.ttf"
default_image = res_path+"default.jpg"
default_music = res_path+"Journey.mp3"
default_poem_font = res_path+"STXINWEI.TTF"

#circle_mask = VideoFileClip('./res/circle_open_center.mov',has_mask=True).to_mask()



current_time = 0
clips=[]
file_clips=[]

def addClip( newClip, duration_time):
    global current_time
    clips.append(newClip.set_start(current_time-crossTime).set_duration(duration_time+crossTime).crossfadein(1))
    current_time = current_time + duration_time

def get_gif(clips,pic_num,gif_num,gif_id,gif_size,gif_position,pick_time,k):
    watermark=clips
    i=0
    t=0
    print(pic_num,gif_num,gif_id,gif_size,gif_position,pick_time,k)
    while t!=gif_num[k]:
        watermark.append(VideoFileClip(gif_id[i], has_mask=True).resize(height=gif_size[i]).set_fps(5).set_duration(pick_time).set_start(
            0).set_position((gif_position[i][0], gif_position[i][1])))
        i=i+1
        t=t+1
    return watermark

def exportTmpFile(in_clip):
    try:
        out_name=tmp_path+str(int(time.time()*1000))+".mp4"
        print(out_name)
        in_clip.write_videofile(out_name,fps=5)
        file_clips.append(out_name)
        print(out_name)
        return out_name
    except Exception as e:
        return e
    #,codec='rawvideo',ffmpeg_params=['-c','copy']


def generate_background_image(image_path):
    #print(image_path)
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    # 先裁剪为16：9
    if width / height > 16 / 9:  # 以长为基准
        target_width = height / 9 * 16
        start_width = (width - target_width) / 2
        img_crop = img.crop((start_width, 0, start_width + target_width, height))  # 左上右下
        print((1, target_width, height))
    elif width / height < 16 / 9:  # 以宽为基准
        target_height = width / 16 * 9
        start_height = (height - target_height) / 2
        img_crop = img.crop((0, start_height, width, start_height + target_height))  # 左上右下
        print((2, width, target_height))
    else:
        img_crop = img
    # 再调整大小，高斯模糊
    img_crop = img_crop.resize((1920, 1080)).filter(ImageFilter.GaussianBlur(8))
    # 减弱颜色
    img_crop = ImageEnhance.Color(img_crop).enhance(0.6)
    return img_crop

def cut_to_cover(image_path):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    # 先裁剪为16：9
    if width / height > 16 / 9:  # 以长为基准
        target_width = height / 9 * 16
        start_width = (width - target_width) / 2
        img_crop = img.crop((start_width, 0, start_width + target_width, height))  # 左上右下
        print((1, target_width, height))
    elif width / height < 16 / 9:  # 以宽为基准
        target_height = width / 16 * 9
        start_height = (height - target_height) / 2
        img_crop = img.crop((0, start_height, width, start_height + target_height))  # 左上右下
        print((2, width, target_height))
    else:
        img_crop = img
    # 再调整大小，高斯模糊
    img_crop = img_crop.resize((1920, 1080)).filter(ImageFilter.GaussianBlur(2))
    return img_crop

def generateCover(np_frame,path):
    img = Image.fromarray(np.uint8(np_frame)).convert('RGB')
    img = img.crop((320, 180, 1600, 900)) 
    img.save(path)



rotMatrix = lambda a: np.array([[np.cos(a), np.sin(a)],
                                [-np.sin(a), np.cos(a)]])


# 标题动画，有BUG 不用了

def vortex(screenpos, i, nletters):
    d = lambda t: 1.0 / (0.3 + t ** 8)  # damping
    a = i * np.pi / nletters  # angle of the movement
    v = rotMatrix(a).dot([-1, 0])
    if i % 2: v[1] = -v[1]
    return lambda t: screenpos + 400 * d(t) * rotMatrix(0.5 * d(t) * a).dot(v)


def cascade(screenpos, i, nletters):
    v = np.array([0, -1])
    d = lambda t: 1 if t < 0 else abs(np.sinc(t) / (1 + t ** 4))
    return lambda t: screenpos + v * 400 * d(t - 0.15 * i)


def arrive(screenpos, i, nletters):
    v = np.array([-1, 0])
    d = lambda t: max(0, 3 - 3 * t)
    return lambda t: screenpos - 400 * v * d(t - 0.2 * i)


def vortexout(screenpos, i, nletters):
    d = lambda t: max(0, t)  # damping
    a = i * np.pi / nletters  # angle of the movement
    v = rotMatrix(a).dot([-1, 0])
    if i % 2: v[1] = -v[1]
    return lambda t: screenpos + 400 * d(t - 0.1 * i) * rotMatrix(-0.2 * d(t) * a).dot(v)


def moveLetters(letters, funcpos):
    return [letter.set_pos(funcpos(letter.screenpos, i, len(letters)))
            for i, letter in enumerate(letters)]
