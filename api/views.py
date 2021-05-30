from django.shortcuts import render
from django.http import HttpResponse,HttpResponseForbidden
from travel.codes import return200,return403,returnList
from django.core.serializers import serialize
from travel.modules.get_color import getColor
from travel.modules.location import coordinate2address,emptydict
from api.modules.FSRCNN.fsrcnn import itFSRCNN
from api.modules.style.neural_style import stylize
import json
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from PIL import Image
import base64


def index(request):
    return render(request,'default.html')

def getColorFunc(request):
    image = request.FILES.get('image',None)
    if not image:
        return return403('未获取到image')
    img = Image.open(image).resize((50, 50)).convert('RGB')  # 取图片数据
    img_byte = BytesIO()
    img.save(img_byte, format='PNG')
    k = request.POST.get("k")
    if k :
        k=int(k)
    else:
        k=2
    result = getColor(img_byte.getvalue(),k)
    for i in result:
        i.reverse()
    return_obj = {
        "k" : k,
        "result" : result
    }   
    return returnList(return_obj)

def FSRCNNFunc(request):
    image = request.FILES.get('image',None)
    if not image:
        return return403('未获取到image')
    scale = request.POST.get("scale")
    if scale :
        scale=int(scale)
        if not (scale in [2,3,4]):
            return return403('缩放倍数错误')
    else:
        scale=3
    opened_image = Image.open(image).convert('RGB')
    opened_image.thumbnail((2160,2160))
    res_img = itFSRCNN(opened_image,scale)
    stream = BytesIO()
    res_img.save(stream, 'JPEG')
    base64_img = base64.b64encode(stream.getvalue()).decode()
    return_data =  base64_img
    return returnList(return_data)


def weatherFunc(request):
    from travel.load_files import weather_model
    image = request.FILES.get('image',None)
    if not image:
        return return403('未获取到image')
    tran1 = transforms.ToTensor()
    tran2 = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    img = Image.open(image).resize((96, 96)).convert('RGB')  # 取图片数据
    img = tran2(tran1(img)).unsqueeze(0).to('cpu')
    pred = weather_model(img)
    pred = torch.softmax(pred,dim=1)
    rate_list = pred.detach().numpy().tolist()[0]
    weather_tags = ['多云', '雨', '雪', '晴']
    sorted_rate, sorted_tag = zip(*sorted(zip(rate_list, weather_tags),reverse=True))

    max_tag = torch.argmax(pred, dim=1)
    
    return_obj = {
        'weather' : weather_tags[int(max_tag)],
        'tags':  sorted_tag,
        'rate': sorted_rate
    }
    return returnList(return_obj)
import os
from io import BytesIO

def getInfo(request):   #debug only
    img_path = "./test/img/"
    #tmp_path = "./test/tmp/"
    img_name = os.listdir(img_path)
    img_list = [ img_path+i
	    for i in img_name]
    img_num = len(img_list)
    color = []
    weather = []
    for i in img_list:
        print(i)
        print(os.path.exists(i))

        
        tran1 = transforms.ToTensor()
        tran2 = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        img = Image.open(i).resize((96, 96)).convert('RGB')  # 取图片数据
        img_byte = BytesIO()
        img.save(img_byte, format='PNG')
        img = tran2(tran1(img)).unsqueeze(0).to('cpu')
        pred = weather_model(img)
        pred = torch.softmax(pred,dim=1)
        weather_tag = torch.argmax(pred, dim=1)
        weather.append(int(weather_tag))

        color.append(getColor(img_byte.getvalue(),1))

    return_obj = {
        'img_num' : img_num,
        'img_name' : img_name,
        'color' : color,
        'weather':  weather
    }
    print(img_num)
    print(img_name)
    print(color)
    print(weather)

    return returnList(return_obj)

def getLocation(request):
    if request.method == "GET":
        print(request.GET)
        longitude = request.GET.get("longitude")
        latitude = request.GET.get("latitude")
        if not (longitude and latitude) :
            return return403("经纬度参数错误")
        return returnList(coordinate2address(float(longitude),float(latitude)))
    else:
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")
        if ((longitude==None) or (latitude==None)) :
            return return403("经纬度参数错误")
        try:
            long_list = longitude.split(",")
            lat_list = latitude.split(",")
            list_len = len(long_list)
            return_obj = []
            for i in range(list_len):
                if not(long_list[i] and lat_list[i]):
                    return_obj.append(emptydict())
                else:
                    return_obj.append(coordinate2address(float(long_list[i]),float(lat_list[i])))
            print("逆地理信息编码完成："+str(list_len))
            return returnList(return_obj)
        except Exception as e:
            return return403("在处理过程中发生了错误："+repr(e))

def getPoem(request):
    from travel.load_files import generatePoet
    keyword = request.POST.get("keyword")
    if not keyword:
        return render(request,'poem.html')
    length = request.POST.get("length")
    if not length:
        experience = 5
    experience = request.POST.get("experience")
    if not experience:
        experience = 1
    history = request.POST.get("history")
    if not history:
        history = 0
    return_obj = []
    for i in range(2):
        result = generatePoet(keyword,int(length),int(experience),int(history))
        if result:
            return_obj.append(result)
    return returnList(return_obj)

def genPoemFromImg(request):
    from travel.load_files import generatePoet
    from travel.resources.cn_dict import cn_dict
    types = request.POST.get("types")
    values = request.POST.get("values")
    image = request.FILES.get('image',None)
    if not (types and values and image):
        return return403('缺少types或values或image')
    fac_name = types.split(",")
    fac_rate = values.split(",")
    length = request.POST.get("length")
    if not length:
        length = 5
    length = int(length)
    experience = request.POST.get("experience")
    if not experience:
        experience = 1
    experience = int(experience)
    history = request.POST.get("history")
    if not history:
        history = 0
    history = int(history)

    from travel.load_files import weather_model
    tran1 = transforms.ToTensor()
    tran2 = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    img = Image.open(image).resize((96, 96)).convert('RGB')  # 取图片数据
    img = tran2(tran1(img)).unsqueeze(0).to('cpu')
    pred = weather_model(img)
    pred = torch.softmax(pred,dim=1)
    weather_specises = ['云', '雨', '雪', '晴']
    weather_tag = torch.argmax(pred, dim=1)
    rate_list = pred.detach().numpy().tolist()[0]
    
    keyword = weather_specises[weather_tag] + " " + cn_dict[fac_name[2]]
    if(float(fac_rate[1])>0.1):
        keyword = keyword+" "+cn_dict[fac_name[1]]
    if(float(fac_rate[0])>0.1):
        keyword = keyword+" "+cn_dict[fac_name[0]]
    res_poem = ""
    
    for i in range(5):
            result = generatePoet(keyword,length,experience,history)
            if result:
                res_poem = result
                break
    
    return_obj = {
        'poem' : res_poem,
        'keywords' : keyword
    }
    return returnList(return_obj)


def getTest(request):
    import synonyms as sy
    a='牡丹'
    b='牡丹'
    s=sy.compare(a,b,seg=True)
    print(s)
    s=sy.compare(a,b,seg=True)
    print(s)
    s=sy.compare(a,b,seg=True)
    print(s)
    return HttpResponse(str(s))


def stylizePhoto(request):
    image = request.FILES.get('image',None)
    if not image:
        return return403('未获取到image')
    from travel.load_files import styles
    style = request.POST.get("style")
    if not style :
        style = random.sample(list(styles.keys()),1)[0]
    if style not in styles:
        return return403("指定的风格不存在："+str(styles.keys()))
    opened_image = Image.open(image).convert('RGB')
    opened_image.thumbnail((1024,1024))
    res_img = stylize(opened_image,styles[style])
    stream = BytesIO()
    res_img.save(stream, 'JPEG')
    base64_img = base64.b64encode(stream.getvalue()).decode()
    return_data =  base64_img
    return returnList(return_data)
