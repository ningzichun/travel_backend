
from travel.modules.get_color import getColor
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from PIL import Image
from .genetic import geneticMain

import os
from io import BytesIO

def getInfo(image_paths):
    from travel.load_files import weather_model
    color = []
    weather = []
    for i in image_paths:
        # print(i)
        # if not os.path.exists(i):
        #     print(i)
        tran1 = transforms.ToTensor()
        tran2 = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        img = Image.open(i).resize((96, 96)).convert('RGB')  # 取图片数据
        img_byte = BytesIO()
        img.save(img_byte, format='PNG')
        img = tran2(tran1(img)).unsqueeze(0).to('cpu')
        pred = weather_model(img)   # 天气识别
        pred = torch.softmax(pred,dim=1)
        weather_tag = torch.argmax(pred, dim=1)
        weather.append(int(weather_tag))
        result = getColor(img_byte.getvalue(),1)
        for i in result:
            i.reverse()
        color.append(result[0])   #主题色 k=1
    return(weather,color)
    #FromHere(img_num,img_name,weather,color)


if __name__=='__main__':
    #print(getInfo())   
    print("IS MAIN")
