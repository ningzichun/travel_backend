from django.shortcuts import render
from forum.models import Post,Comment
from django.core.serializers import serialize
from travel.codes import return200,return403,returnList
from django.utils import timezone
from datetime import datetime
from user.models import User
from photo.models import Photo
from photo import tasks
import celery
import random
import shutil
import json
import time
import os

def index(request):
    context={'headers':request.headers}
    return render(request,'default.html',context)

def checkMissingInfo(wid,work_obj):  #检查完整性
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
    #json文件正确性
    if not "images" in load_dict:
        return("info.json 中无 images")
    if not "title" in load_dict:
        return("info.json 中无 title")
    if not "description" in load_dict:
        return("info.json 中无 description")
    work_obj.photo_title = load_dict["title"]
    work_obj.photo_description = load_dict["description"]
    work_obj.save()
    images_in_json = list(load_dict["images"])
    print(images_in_json)
    print(files_in_dir)
    for i in images_in_json:
        if i not in files_in_dir:
            return("缺少文件："+i)
    return False

def newWork(request):   #新建作业集
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    uid_obj = User.objects.filter(uid=uid).first()
    work_obj = Photo(uid=uid_obj,status_msg='等待用户提供信息',create_time=timezone.now(),update_time=timezone.now())
    work_obj.save()
    str_wid = str(work_obj.work_id)
    dir_path = "./media/photos/"+str_wid
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return_data = {
        'work_id' : work_obj.work_id
    }
    return returnList(return_data)


def uploadImage(request,wid):   #上传图片到文件夹中
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Photo.objects.filter(uid = uid,work_id=wid).first()
    if not work_obj:
        return return403('找不到作业集')
    str_wid=str(wid)
    file = request.FILES.get('file',None)
    if not file:
        return return403('未获取到file')
    f, e = os.path.splitext(file.name)
    destination = open(os.path.join("media/photos/"+str_wid,file.name),'wb+')    # 打开特定的文件进行二进制的写操作 
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
    work_obj = Photo.objects.filter(uid = uid,work_id=wid).first()
    if not work_obj:
        return return403('找不到作业集')
    img_path = "./media/photos/"+str(wid)
    if not os.path.exists(img_path):    #找不到目录，已过期
        work_obj.status = -2
        work_obj.status_msg = '已过期'
        work_obj.save()
    if work_obj.status == -2 :
        return return403("长图已过期，请重新新建")
    # 检查是否已经开始，以及是否未正常退出
    if work_obj.status == 200 :
        return return403("任务已完成")
    if work_obj.status > 0 :    # 已开始，检查状态
        try:
            task_obj = celery.result.AsyncResult(work_obj.result_msg) # 存在状态记录，无需重新运行
            if task_obj.status=='FAILURE':
                ret_desc = "排队等待中"
                ret_msg = "原执行失败，在 FAILURE 队列，已重新加入等待队列"
            else: 
                return return403("已在 "+task_obj.state+" 队列中")
        except Exception:   # 查询不到记录，重新执行
            ret_desc = "排队等待中"
            ret_msg = "已重新加入队列"
    elif work_obj.status == -1:   # 前期执行失败
        ret_desc = "排队等待中"
        ret_msg = "原执行失败，已重新加入队列"
    else:
        ret_desc = "排队等待中"
        ret_msg = "已加入队列"
    hasMissingInfo = checkMissingInfo(wid,work_obj)
    if hasMissingInfo:
        return return403(hasMissingInfo)
    work_obj.status = 100
    work_obj.status_msg = ret_desc
    newTask = tasks.makePhoto.delay(wid,uid)
    work_obj.result_msg = newTask.task_id
    work_obj.save()
    return return200(ret_msg)

def getStatus(request,wid): #获取当前状态
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Photo.objects.filter(uid = uid,work_id=wid).first()
    if not work_obj:
        return return403('找不到作业集')
    img_path = "./media/photos/"+str(wid)
    image_urls = [];image_num = 0
    
    if not os.path.exists(img_path):    #找不到目录，已过期
        work_obj.status = -2
        work_obj.status_msg = '已过期'
        work_obj.save()
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
            work_obj.status_msg = 'info.json 缺失'

        image_num = len(image_urls)

    if (work_obj.status > 0) and (work_obj.status < 200) :  #已开始，非成功状态
        try:
            task_obj = celery.result.AsyncResult(work_obj.result_msg)
        except Exception:   # 无任务ID
            work_obj.status = -1
            work_obj.status_msg = '找不到任务，请重新启动'
            work_obj.save()
        else:
            if task_obj.status=='FAILURE':
                work_obj.status = -1
                work_obj.status_msg = '上次执行失败于：'+work_obj.status_msg
                work_obj.save()
            print(task_obj.state)
            print(task_obj.result)
    return_data = {
        'work_id' : work_obj.work_id,
        'uid' : work_obj.uid.uid,
        'photo_title' : work_obj.photo_title,
        'photo_description' : work_obj.photo_description,
        'photo_cover' : work_obj.photo_cover,
        'create_time' : work_obj.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time' : work_obj.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        'status' : work_obj.status,
        'status_msg' : work_obj.status_msg,
        'result_msg' : work_obj.result_msg,
        'image_num' : image_num,
        'image_urls' :image_urls
    }
    return returnList(return_data)

def deletePhoto(request,wid):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Photo.objects.filter(uid = uid,work_id=wid).first()
    if not work_obj:
        return return403('找不到作业集')
    str_wid=str(wid)

    img_path = "./media/photos/"+str(wid)
    if not os.path.exists(img_path):    #找不到目录
        work_obj.status = -2
        work_obj.status_msg = '已过期'
        work_obj.save()
        return return200('文件夹不存在，可能已删除')
    shutil.rmtree(img_path)
    work_obj.status = -2
    work_obj.status_msg = '已过期'
    work_obj.save()
    return return200('删除成功')


def myPhotoList(request):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Photo.objects.filter(uid = uid,status__gt=0)

    return_data = {
        'uid' : uid,
        'photo_num' : work_obj.count(),
        'photos' : []
    }

    for i in work_obj:
        return_data['photos'].append({
            'work_id': i.work_id,
            'photo_title' : i.photo_title,
            'photo_description' : i.photo_description,
            'photo_cover' : i.photo_cover,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
        })
    
    return returnList(return_data)

def myPhotoListAll(request):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Photo.objects.filter(uid = uid)

    return_data = {
        'uid' : uid,
        'photo_num' : work_obj.count(),
        'photos' : []
    }

    for i in work_obj:
        return_data['photos'].append({
            'work_id': i.work_id,
            'photo_title' : i.photo_title,
            'photo_description' : i.photo_description,
            'photo_cover' : i.photo_cover,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
        })
    
    return returnList(return_data)

def photoListAll(request):
    work_obj = Photo.objects.filter()

    return_data = {
        'photo_num' : work_obj.count(),
        'photos' : []
    }

    for i in work_obj:
        return_data['photos'].append({
            'work_id': i.work_id,
            'uid' : i.uid.uid,
            'uname' : i.uid.uname,
            'photo_title' : i.photo_title,
            'photo_description' : i.photo_description,
            'photo_cover' : i.photo_cover,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
        })
    
    return returnList(return_data)

def sharePhoto(request,wid):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Photo.objects.filter(uid = uid,work_id=wid).first()
    if not work_obj:
        return return403('找不到作业集')
    if work_obj.status!=200:
        return return403('成功生成的长图才可分享')
    title = work_obj.photo_title
    text =  work_obj.photo_description
    cover = work_obj.photo_cover
    photo_info={
        'work_id': work_obj.work_id,
        'photo_title' : work_obj.photo_title,
        'photo_description' : work_obj.photo_description,
        'photo_cover' : work_obj.photo_cover,
        'create_time' : work_obj.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time' : work_obj.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        'status' : work_obj.status,
        'status_msg' : work_obj.status_msg,
        'result_msg' : work_obj.result_msg,
    }
    post_type = 3
    uid_obj=User.objects.filter(uid=uid).first()
    photo_info_str = json.dumps(photo_info)
    post_obj=Post(uid=uid_obj,title=title,post_type=post_type,text=text,time=datetime.now(),cover=cover,reference=photo_info_str)
    post_obj.save()
    return return200("分享成功")

def shareFunc(uid,photo_info):
    title = photo_info["photo_title"]
    text =  photo_info["photo_description"]
    cover = photo_info["photo_cover"]
    post_type = 3
    uid_obj=User.objects.filter(uid=uid).first()
    photo_info_str = json.dumps(photo_info)
    post_obj=Post(uid=uid_obj,title=title,post_type=post_type,text=text,time=datetime.now(),cover=cover,reference=photo_info_str)
    post_obj.save()
