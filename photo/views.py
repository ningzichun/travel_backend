from django.shortcuts import render
from django.core.serializers import serialize
from travel.codes import return200,return403,returnList
from django.utils import timezone
from datetime import datetime
from user.models import User
from photo.models import Photo,PhotoComment
from photo import tasks
from django.core.cache import cache
from travel.resources.postcode import code2img
from travel.modules.location import coordinate2image
from travel.resources.cn_dict import cn_dict
from PIL import Image, ImageDraw, ImageFont
import traceback
import celery
import random
import shutil
import json
import time
import os

def index(request):
    context={'headers':request.headers}
    return render(request,'default.html',context)

def checkMissingInfo(wid,photo_obj):  #检查完整性
    dir_path = "./media/photos/"+str(wid)
    files_in_dir = os.listdir(dir_path)
    #json文件存在性
    try:
        with open("./media/photos/"+str(wid)+"/info.json",'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            print(load_dict)
    except FileNotFoundError:
        return("info.json 不存在")
    except Exception:
        return("info.json 读取失败")
    if not "share" in load_dict:
        load_dict["share"] = True
    elif load_dict["share"]:
        load_dict["share"] = True
    else :
        load_dict["share"] = False
    #json文件正确性
    if not "images" in load_dict:
        return("info.json 中无 images")
    if not "title" in load_dict:
        return("info.json 中无 title")
    if not "description" in load_dict:
        return("info.json 中无 description")
    photo_obj.photo_title = load_dict["title"]
    photo_obj.photo_description = load_dict["description"]
    photo_obj.share_tag = load_dict["share"]
    photo_obj.save()
    images_in_json = list(load_dict["images"])
    print(images_in_json)
    print(files_in_dir)
    for i in images_in_json:
        if i not in files_in_dir:
            return("缺少文件："+i)
    return False

def newPhoto(request):   #新建作业集
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    uid_obj = User.objects.filter(uid=uid).first()
    photo_obj = Photo(uid=uid_obj,status_msg='等待用户提供信息',create_time=timezone.now(),update_time=timezone.now())
    photo_obj.save()
    str_wid = str(photo_obj.work_id)
    dir_path = "./media/photos/"+str_wid
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return_data = {
        'work_id' : photo_obj.work_id
    }
    return returnList(return_data)


def uploadImage(request,wid):   #上传图片到文件夹中
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    photo_obj = Photo.objects.filter(uid = uid,work_id=wid).first()
    if not photo_obj:
        return return403('找不到作业集')
    str_wid=str(wid)
    file = request.FILES.get('file',None)
    if not file:
        return return403('未获取到file')
    #f, e = os.path.splitext(file.name)
    filename = file.name
    try:
        opened_image = Image.open(file)
        opened_image.convert("RGB")
        w,h = opened_image.size
        print("("+str(w)+","+str(h)+")")
        if h<300:
            scale = 300/h
            opened_image = opened_image.resize((w*scale,300))
            opened_image.save("media/photos/"+str_wid+"/"+filename)
            print("Height Resized")
        elif w<300:
            scale = 300/h
            opened_image = opened_image.resize((300,h*scale))
            opened_image.save("media/photos/"+str_wid+"/"+filename)
            print("Width Resized")
        else:
            destination = open(os.path.join("media/photos/"+str_wid,filename),'wb+')    # 打开特定的文件进行二进制的写操作 
            for chunk in file.chunks():      # 分块写入文件 
                destination.write(chunk) 
            destination.close() 
    except Exception as e:
        destination = open(os.path.join("media/photos/"+str_wid,filename),'wb+')    # 打开特定的文件进行二进制的写操作 
        for chunk in file.chunks():      # 分块写入文件 
            destination.write(chunk) 
        destination.close() 
    return_data = {
        'filename' : file.name,
        'url' : "/media/photos/"+str_wid+"/"+file.name
    }
    return returnList(return_data)


def startPhoto(request,wid): #开始生成长图
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    photo_obj = Photo.objects.filter(uid = uid,work_id=wid).first()
    if not photo_obj:
        return return403('找不到作业集')
    img_path = "./media/photos/"+str(wid)
    if not os.path.exists(img_path):    #找不到目录，已过期
        photo_obj.status = -2
        photo_obj.status_msg = '已过期'
        photo_obj.save()
    if photo_obj.status == -2 :
        return return403("长图已过期，请重新新建")
    # 检查是否已经开始，以及是否未正常退出
    if photo_obj.status == 200 :
        return return403("任务已完成")
    if photo_obj.status > 0 :    # 已开始，检查状态
        return return403("任务已启动")
    elif photo_obj.status == -1:   # 前期执行失败
        ret_desc = "排队等待中"
        ret_msg = "原执行失败，已重新加入队列"
    else:
        ret_desc = "排队等待中"
        ret_msg = "已加入队列"
    hasMissingInfo = checkMissingInfo(wid,photo_obj)
    if hasMissingInfo:
        return return403(hasMissingInfo)
    photo_obj.status = 100
    photo_obj.status_msg = ret_desc
    photo_obj.save()
    newTask = tasks.makePhoto.delay(wid,uid)
    print("分配作业",newTask.task_id)
    photo_obj.result_msg = newTask.task_id
    photo_obj.save()
    return return200(ret_msg)

def getStatus(request,wid): #获取当前状态
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    photo_obj = Photo.objects.filter(uid = uid,work_id=wid).first()
    if not photo_obj:
        return return403('找不到作业集')
    img_path = "./media/photos/"+str(wid)
    image_urls = [];image_num = 0
    
    if not os.path.exists(img_path):    #找不到目录，已过期
        photo_obj.status = -2
        photo_obj.status_msg = '已过期'
        photo_obj.save()
        image_num = 0
        image_urls = []
    else:
        try:
            with open("./media/photos/"+str(wid)+"/info.json",'r') as load_f:
                load_dict = json.load(load_f)
                images_in_json = list(load_dict["images"])
                image_urls = [ "/media/photos/"+str(wid)+"/"+i for i in images_in_json] 
                image_num = len(image_urls)
        except FileNotFoundError:
            photo_obj.status_msg = 'info.json 缺失'

        image_num = len(image_urls)

    return_data = {
        'work_id' : photo_obj.work_id,
        'uid' : photo_obj.uid.uid,
        'photo_title' : photo_obj.photo_title,
        'photo_description' : photo_obj.photo_description,
        'photo_cover' : photo_obj.photo_cover,
        'cover_width' : photo_obj.cover_width,
        'cover_height' : photo_obj.cover_height,
        'photo_width' : photo_obj.photo_width,
        'photo_height' : photo_obj.photo_height,
        'create_time' : photo_obj.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time' : photo_obj.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        'status' : photo_obj.status,
        'status_msg' : photo_obj.status_msg,
        'result_msg' : photo_obj.result_msg,
        'image_num' : image_num,
        'image_urls' :image_urls
    }
    return returnList(return_data)


def randStr(length = 4):
    num_set = [chr(i) for i in range(48,58)]
    char_set = [chr(i) for i in range(97,123)]
    total_set = num_set + char_set
    result_set = "".join(random.sample(total_set, length))
    return result_set


def deletePhoto(request,wid):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    photo_obj = Photo.objects.filter(uid = uid,work_id=wid).first()
    if not photo_obj:
        return return403('找不到作业集')
    str_wid=str(wid)

    img_path = "./media/photos/"+str(wid)
    if not os.path.exists(img_path):    #找不到目录
        photo_obj.status = -2
        photo_obj.status_msg = '已过期'
        photo_obj.save()
        return return200('文件夹不存在，可能已删除')
    shutil.rmtree(img_path)
    photo_obj.status = -2
    photo_obj.status_msg = '已过期'
    photo_obj.save()
    return return200('删除成功')


def myPhotoList(request):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    photo_obj = Photo.objects.filter(uid = uid,status__gt=150)

    return_data = {
        'uid' : uid,
        'photo_num' : photo_obj.count(),
        'photos' : []
    }

    for i in photo_obj:
        return_data['photos'].append({
            'work_id': i.work_id,
            'photo_title' : i.photo_title,
            'photo_description' : i.photo_description,
            'photo_cover' : i.photo_cover,
            'cover_width' : i.cover_width,
            'cover_height' : i.cover_height,
            'photo_width' : i.photo_width,
            'photo_height' : i.photo_height,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
            'like_num' : i.like_num,
            'comment_num' : i.comment_num,
        })
    
    return returnList(return_data)

def myPhotoListAll(request):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    photo_obj = Photo.objects.filter(uid = uid)

    return_data = {
        'uid' : uid,
        'photo_num' : photo_obj.count(),
        'photos' : []
    }

    for i in photo_obj:
        return_data['photos'].append({
            'work_id': i.work_id,
            'photo_title' : i.photo_title,
            'photo_description' : i.photo_description,
            'photo_cover' : i.photo_cover,
            'cover_width' : i.cover_width,
            'cover_height' : i.cover_height,
            'photo_width' : i.photo_width,
            'photo_height' : i.photo_height,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
            'like_num' : i.like_num,
            'comment_num' : i.comment_num,
        })
    
    return returnList(return_data)

def photoListAll(request):
    photo_obj = Photo.objects.filter(share_tag = True,status__gt=150)

    return_data = {
        'photo_num' : photo_obj.count(),
        'photos' : []
    }

    for i in photo_obj:
        return_data['photos'].append({
            'work_id': i.work_id,
            'uid' : i.uid.uid,
            'uname' : i.uid.uname,
            'avatar' : '/media/'+i.uid.avatar.name,
            'photo_title' : i.photo_title,
            'photo_description' : i.photo_description,
            'photo_cover' : i.photo_cover,
            'cover_width' : i.cover_width,
            'cover_height' : i.cover_height,
            'photo_width' : i.photo_width,
            'photo_height' : i.photo_height,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
            'like_num' : i.like_num,
            'comment_num' : i.comment_num,
        })
    
    return returnList(return_data)

def likePhoto(request,wid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    photo_obj = Photo.objects.filter(work_id=wid).first()
    if not photo_obj:
        return return403('找不到影集')
    
    cached = cache.get(str(uid)+'photo'+str(wid))
    if cached:
        return return403('已经点过赞啦~')
    
    photo_obj.like_num = photo_obj.like_num + 1
    photo_obj.save()
    cache.set(str(uid)+'photo'+str(wid), 1, 3600)
    return return200('操作成功')


def getComment(request,wid):
    photo_obj = Photo.objects.filter(work_id = wid)
    if not photo_obj:
        return403("找不到长图")

    comments = PhotoComment.objects.filter(photo=photo_obj)
    return_data = {
        'comment_num' : comments.count(),
        'comments' : []
    }
    for i in comments:
        return_data['comments'].append({
            'comment_id': i.comment_id,
            'uid' : i.uid.uid,
            'uname' : i.uid.uname,
            'gender' : i.uid.gender,
            'avatar' : '/media/'+i.uid.avatar.name,
            'text' : i.text,
            'time' : i.time.strftime("%Y-%m-%d %H:%M:%S"),
            'like_num' : i.like_num,
        })
    return returnList(return_data)


def newComment(request,wid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    wid = int(wid)
    text = request.POST.get("text")
    if not text:
        return return403('参数无效')
    uid_obj = User.objects.filter(uid=uid).first()
    photo_obj = Photo.objects.filter(work_id=wid).first()
    if not photo_obj:
        return return403('找不到长图')
    comment_obj = PhotoComment(uid=uid_obj,photo=photo_obj, text=text,time=timezone.now())
    comment_obj.save()
    return return200('操作成功')


def likeComment(request,cid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    comment_obj = PhotoComment.objects.filter(comment_id=cid).first()
    if not comment_obj:
        return return403('找不到评论')
    
    cached = cache.get(str(uid)+'pcom'+str(cid))
    if cached:
        return return403('已经点过赞啦~')
    
    comment_obj.like_num = comment_obj.like_num + 1
    comment_obj.save()

    cache.set(str(uid)+'pcom'+str(cid), 1, 3600)
    return return200('操作成功')

def deleteComment(request,cid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    comment_obj = PhotoComment.objects.filter(comment_id=cid,uid=uid).first()
    if not comment_obj:
        return return403('找不到评论')
    comment_obj.delete()
    return return200('操作成功')


def getLocationImage(long,lat):
    return True
