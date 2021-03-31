import json


def makeMovie():
    work_dir = './img'
    with open( work_dir + "/info.json",'r') as load_f:
        load_dict = json.load(load_f)
    images_in_json = list(load_dict["images"])
    image_paths = [ work_dir+"/"+i for i in images_in_json]
    factors = load_dict["factors"]
    print(image_paths)
    print(factors)

    img_num = len(images_in_json)
    print(img_num,images_in_json)
            
    weather,color = getInfo(image_paths)

    ## 生成影集代码
    from genetic import FromHere
    FromHere(img_num,image_paths,weather,color,load_dict)
    print("Finish.")


import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from PIL import Image
from .genetic import FromHere

import os
from io import BytesIO

def getInfo(image_paths):
    from codes.load_files import weather_model
    from codes.get_color import getColor
    color = []
    weather = []
    for i in image_paths:
        print(i)
        if not os.path.exists(i):
            print(i)
        tran1 = transforms.ToTensor()
        tran2 = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        img = Image.open(i).resize((96, 96)).convert('RGB')  # 取图片数据
        img_byte = BytesIO()
        img.save(img_byte, format='PNG')
        img = tran2(tran1(img)).unsqueeze(0).to('cpu')
        pred = weather_model(img)   # 天气识别
        weather_tag = torch.argmax(pred, dim=1)
        weather.append(int(weather_tag))
        color.append(getColor(img_byte.getvalue(),1)[0])   #主题色 k=1
    return(weather,color)

if __name__=='__main__':
    makeMovie()
