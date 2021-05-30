import os
from PIL import Image, ImageFilter, ImageEnhance,ImageDraw
from moviepy.editor import *
import numpy as np
import time
from random import randint
from .filelist import *

screensize = (1920, 1080)
crossTime = 1

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
    # print(pic_num,gif_num,gif_id,gif_size,gif_position,pick_time,k)
    while t!=gif_num[k]:
        watermark.append(VideoFileClip(gif_id[i], has_mask=True).resize(height=gif_size[i]).set_fps(5).set_duration(pick_time).set_start(
            0).set_position((gif_position[i][0], gif_position[i][1])))
        i=i+1
        t=t+1
    return watermark

def exportTmpFile(in_clip,fps):
    try:
        out_name=tmp_path+str(int(time.time()*1000))+".mp4"
        # print(out_name)
        in_clip.write_videofile(out_name,fps=fps)
        file_clips.append(out_name)
        # print(out_name)
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
        # print((1, target_width, height))
    elif width / height < 16 / 9:  # 以宽为基准
        target_height = width / 16 * 9
        start_height = (height - target_height) / 2
        img_crop = img.crop((0, start_height, width, start_height + target_height))  # 左上右下
        # print((2, width, target_height))
    else:
        img_crop = img
    # 再调整大小，高斯模糊
    img_crop = img_crop.resize((1920, 1080)).filter(ImageFilter.GaussianBlur(12))
    # 减弱颜色
    img_crop = ImageEnhance.Color(img_crop).enhance(0.7)
    return img_crop

def cut_to_cover(image_path):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    # 先裁剪为16：9
    if width / height > 16 / 9:  # 以长为基准
        target_width = height / 9 * 16
        start_width = (width - target_width) / 2
        img_crop = img.crop((start_width, 0, start_width + target_width, height))  # 左上右下
        # print((1, target_width, height))
    elif width / height < 16 / 9:  # 以宽为基准
        target_height = width / 16 * 9
        start_height = (height - target_height) / 2
        img_crop = img.crop((0, start_height, width, start_height + target_height))  # 左上右下
        # print((2, width, target_height))
    else:
        img_crop = img
    # 再调整大小，高斯模糊
    img_crop = img_crop.resize((1920, 1080)).filter(ImageFilter.GaussianBlur(2))
    return img_crop

def cut_to_size(target_w,target_h,image_path):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    rate = target_w / target_h
    # 先裁剪为16：9
    if width / height > rate:  # 以长为基准
        target_width = int(height / target_h * target_w)
        start_width = int((width - target_width) / 2)
        img_crop = img.crop((start_width, 0, start_width + target_width, height))  # 左上右下
        # print((1, target_width, height))
    elif width / height < rate:  # 以宽为基准
        target_height = int(width / target_w * target_h)
        start_height = int((height - target_height) / 2)
        img_crop = img.crop((0, start_height, width, start_height + target_height))  # 左上右下
        # print((2, width, target_height))
    else:
        img_crop = img
    # 再调整大小，高斯模糊
    img_crop = img_crop.resize((target_w, target_h))
    return img_crop

def generateCover(np_frame,path):
    img = Image.fromarray(np.uint8(np_frame)).convert('RGB')
    #img = img.crop((320, 180, 1600, 900)) 
    img.save(path)

def circle_corner(img, radii):  #把原图片变成圆角
    """
    :param radii: 半径，如：30。
    """
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
    # 原图
    img = img.convert("RGBA")
    w, h = img.size
    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()
    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img

def cut_with_border(target_w1,target_h1,image_path):
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    target_w = target_w1 -20
    target_h = target_h1 -20
    rate = target_w / target_h
    # 先裁剪为16：9
    if width / height > rate:  # 以长为基准
        target_width = int(height / target_h * target_w)
        start_width = int((width - target_width) / 2)
        img_crop = img.crop((start_width, 0, start_width + target_width, height))  # 左上右下
        # print((1, target_width, height))
    elif width / height < rate:  # 以宽为基准
        target_height = int(width / target_w * target_h)
        start_height = int((height - target_height) / 2)
        img_crop = img.crop((0, start_height, width, start_height + target_height))  # 左上右下
        # print((2, width, target_height))
    else:
        img_crop = img
    # 再调整大小
    img_crop = img_crop.resize((target_w, target_h))
    img2 = Image.new(img.mode, (target_w1, target_h1),'white')
    img2.paste(circle_corner(img_crop,20), (10, 10))
    # img3 = circle_corner(img2,20)
    # img3.show()
    return img2

def limit_hw_border(target_w1,target_h1,image_path,border_size=10):
    img = Image.open(image_path).convert('RGBA')
    target_w = target_w1 - border_size - border_size
    target_h = target_h1 - border_size - border_size
    width, height = img.size
    if width < target_w:
        rate = target_w / target_h
        # 先裁剪为16：9
        if width / height > rate:  # 以长为基准
            target_width = int(height / target_h * target_w)
            start_width = int((width - target_width) / 2)
            img = img.crop((start_width, 0, start_width + target_width, height))  # 左上右下
        elif width / height < rate:  # 以宽为基准
            target_height = int(width / target_w * target_h)
            start_height = int((height - target_height) / 2)
            img = img.crop((0, start_height, width, start_height + target_height))  # 左上右下
    else:
        img.thumbnail((target_w,target_h))
    img2 = Image.new(img.mode, (target_w1, target_h1),'white')
    img2.paste(circle_corner(img,20), (border_size, border_size))
    return img2

