from django.shortcuts import render
from django.http import HttpResponse,HttpResponseForbidden
from travel.codes import return200,return403,returnList
from django.core.serializers import serialize
from travel.modules.get_color import getColor
from travel.modules.location import coordinate2address
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from PIL import Image


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
    scale = request.POST.get("k")
    if scale :
        scale=int(scale)
    else:
        scale=4
    itFSRCNN(image,scale)
    return return200("1")


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
    weather_specises = ['cloudy', 'rainy', 'snow', 'sunny']
    weather_tag = torch.argmax(pred, dim=1)
    rate_list = pred.detach().numpy().tolist()[0]
    return_obj = {
        'weather' : weather_specises[int(weather_tag)],
        'weather_id' : int(weather_tag),
        'tags':  weather_specises,
        'rate': rate_list
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
        if not (longitude and latitude) :
            return return403("经纬度参数错误")
        try:
            long_list = longitude.split(",")
            lat_list = latitude.split(",")
            list_len = len(long_list)
            return_obj = []
            for i in range(list_len):
                print(float(long_list[i]),float(lat_list[i]))
                return_obj.append(coordinate2address(float(long_list[i]),float(lat_list[i])))
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
