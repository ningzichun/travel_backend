from django.shortcuts import render
from django.core.serializers import serialize
from travel.codes import return200,return403,returnList
from django.utils import timezone
from datetime import datetime
from user.models import User
from movie.models import Work,WorkComment
from movie import tasks

from django.core.cache import cache
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
    dir_path = "./media/movies/"+str(wid)
    files_in_dir = os.listdir(dir_path)
    #json文件存在性
    try:
        with open("./media/movies/"+str(wid)+"/info.json",'r',encoding='utf-8') as load_f:
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
    if not "share" in load_dict:
        load_dict["share"] = True
    elif load_dict["share"]:
        load_dict["share"] = True
    else :
        load_dict["share"] = False
    if not "tag" in load_dict:
        load_dict["tag"] = 1
    work_obj.movie_title = load_dict["title"]
    work_obj.movie_description = load_dict["description"]
    work_obj.share_tag = load_dict["share"]
    work_obj.tag = int(load_dict["tag"])
    work_obj.save()
    images_in_json = list(load_dict["images"])
    for i in images_in_json:
        if i not in files_in_dir:
            return("缺少文件："+i)
    print("合法性检测通过")
    return False

def newWork(request):   #新建作业集
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    uid_obj = User.objects.filter(uid=uid).first()
    work_obj = Work(uid=uid_obj,status_msg='等待用户提供信息',create_time=timezone.now(),update_time=timezone.now())
    work_obj.save()
    str_wid = str(work_obj.work_id)
    dir_path = "./media/movies/"+str_wid
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
    work_obj = Work.objects.filter(uid = uid,work_id=wid).first()
    if not work_obj:
        return return403('找不到作业集')
    str_wid=str(wid)
    file = request.FILES.get('file',None)
    if not file:
        return return403('未获取到file')
    f, e = os.path.splitext(file.name)
    #imgName=str(int(time.time()*100))+f+e #去掉原文件名特征
    #imgName=str(int(time.time()*100))+str(random.randint(1000,9999))+e
    #file.name = imgName
    destination = open(os.path.join("media/movies/"+str_wid,file.name),'wb+')    # 打开特定的文件进行二进制的写操作 
    for chunk in file.chunks():      # 分块写入文件 
        destination.write(chunk) 
    destination.close() 
    return_data = {
        'filename' : file.name,
        'url' : "/media/movies/"+str_wid+"/"+file.name
    }
    return returnList(return_data)


def startWork(request,wid): #开始生成影集
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Work.objects.filter(uid = uid,work_id=wid).first()
    if not work_obj:
        return return403('找不到作业集')
    print("请求生成影集")
    img_path = "./media/movies/"+str(wid)
    if not os.path.exists(img_path):    #找不到目录，已过期
        work_obj.status = -2
        work_obj.status_msg = '已过期'
        work_obj.save()
    if work_obj.status == -2 :
        return return403("影集已过期，请重新新建")
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
    print("准备分配作业")
    newTask = tasks.makeMovie.delay(wid,uid)
    print("分配作业",newTask.task_id)
    work_obj.result_msg = newTask.task_id
    work_obj.save()
    return return200(ret_msg)

def getStatus(request,wid): #获取当前状态
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Work.objects.filter(uid = uid,work_id=wid).first()
    if not work_obj:
        return return403('找不到作业集')
    img_path = "./media/movies/"+str(wid)
    image_urls = [];image_num = 0
    
    if not os.path.exists(img_path):    #找不到目录，已过期
        work_obj.status = -2
        work_obj.status_msg = '已过期'
        work_obj.save()
        image_num = 0
        image_urls = []
    else:
        try:
            with open("./media/movies/"+str(wid)+"/info.json",'r') as load_f:
                load_dict = json.load(load_f)
                images_in_json = list(load_dict["images"])
                image_urls = [ "/media/movies/"+str(wid)+"/"+i for i in images_in_json] 
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
        'movie_title' : work_obj.movie_title,
        'movie_description' : work_obj.movie_description,
        'movie_cover' : work_obj.movie_cover,
        'create_time' : work_obj.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time' : work_obj.update_time.strftime('%Y-%m-%d %H:%M:%S'),
        'status' : work_obj.status,
        'status_msg' : work_obj.status_msg,
        'result_msg' : work_obj.result_msg,
        'image_num' : image_num,
        'image_urls' :image_urls
    }
    return returnList(return_data)

def deleteMovie(request,wid):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Work.objects.filter(uid = uid,work_id=wid).first()
    if not work_obj:
        return return403('找不到作业集')
    str_wid=str(wid)

    file = request.FILES.get('file',None)
    if not file:
        return return403('未获取到file')
    img_path = "./media/movies/"+str(wid)
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


def myMovieList(request):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Work.objects.filter(uid = uid,status__gt=0)

    return_data = {
        'uid' : uid,
        'movie_num' : work_obj.count(),
        'movies' : []
    }

    for i in work_obj:
        #if (i.status > 0) and (i.status < 200):
        return_data['movies'].append({
            'work_id': i.work_id,
            'movie_title' : i.movie_title,
            'movie_description' : i.movie_description,
            'movie_cover' : i.movie_cover,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
            'tag' : i.tag,
            'like_num' : i.like_num,
            'comment_num' : i.comment_num,
        })
    
    return returnList(return_data)

def myMovieListAll(request):
    uid = request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Work.objects.filter(uid = uid)

    return_data = {
        'uid' : uid,
        'movie_num' : work_obj.count(),
        'movies' : []
    }

    for i in work_obj:
        return_data['movies'].append({
            'work_id': i.work_id,
            'movie_title' : i.movie_title,
            'movie_description' : i.movie_description,
            'movie_cover' : i.movie_cover,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
            'tag' : i.tag,
            'like_num' : i.like_num,
            'comment_num' : i.comment_num,
        })
    
    return returnList(return_data)

def movieListAll(request):
    work_obj = Work.objects.filter(share_tag = True,status__gt=150)

    return_data = {
        'movie_num' : work_obj.count(),
        'movies' : []
    }

    for i in work_obj:
        return_data['movies'].append({
            'work_id': i.work_id,
            'uid' : i.uid.uid,
            'uname' : i.uid.uname,
            'avatar' : '/media/'+i.uid.avatar.name,
            'movie_title' : i.movie_title,
            'movie_description' : i.movie_description,
            'movie_cover' : i.movie_cover,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
            'tag' : i.tag,
            'like_num' : i.like_num,
            'comment_num' : i.comment_num,
        })
    
    return returnList(return_data)

def movieListTag(request,tag):
    work_obj = Work.objects.filter(share_tag = True,status__gt=150,tag = tag)

    return_data = {
        'movie_num' : work_obj.count(),
        'movies' : []
    }

    for i in work_obj:
        return_data['movies'].append({
            'work_id': i.work_id,
            'uid' : i.uid.uid,
            'uname' : i.uid.uname,
            'avatar' : '/media/'+i.uid.avatar.name,
            'movie_title' : i.movie_title,
            'movie_description' : i.movie_description,
            'movie_cover' : i.movie_cover,
            'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status' : i.status,
            'status_msg' : i.status_msg,
            'result_msg' : i.result_msg,
            'tag' : i.tag,
            'like_num' : i.like_num,
            'comment_num' : i.comment_num,
        })
    
    return returnList(return_data)

def likeMovie(request,wid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    work_obj = Work.objects.filter(work_id=wid).first()
    if not work_obj:
        return return403('找不到影集')
    
    cached = cache.get(str(uid)+'work'+str(wid))
    if cached:
        return return403('已经点过赞啦~')
    
    work_obj.like_num = work_obj.like_num + 1
    work_obj.save()
    cache.set(str(uid)+'work'+str(wid), 1, 3600)
    return return200('操作成功')


def getComment(request,wid):
    work_obj = Work.objects.filter(work_id = wid)
    if not work_obj:
        return403("找不到影集")

    comments = WorkComment.objects.filter(work=work_obj)
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
    work_obj = Work.objects.filter(work_id=wid).first()
    if not work_obj:
        return return403('找不到影集')
    comment_obj = WorkComment(uid=uid_obj,work=work_obj, text=text,time=timezone.now())
    comment_obj.save()
    return return200('操作成功')


def likeComment(request,cid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    comment_obj = WorkComment.objects.filter(comment_id=cid).first()
    if not comment_obj:
        return return403('找不到评论')
    
    cached = cache.get(str(uid)+'mcom'+str(cid))
    if cached:
        return return403('已经点过赞啦~')
    
    comment_obj.like_num = comment_obj.like_num + 1
    comment_obj.save()

    cache.set(str(uid)+'mcom'+str(cid), 1, 3600)
    return return200('操作成功')

def deleteComment(request,cid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    comment_obj = WorkComment.objects.filter(comment_id=cid,uid=uid).first()
    if not comment_obj:
        return return403('找不到评论')
    comment_obj.delete()
    return return200('操作成功')

