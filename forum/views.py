from django.shortcuts import render
from forum.models import Post,Comment
from django.core.serializers import serialize
from travel.codes import return200,return403,returnList
from django.utils import timezone
from datetime import datetime
from user.models import User
import json
# Create your views here.

def index(request):

    postNum=Post.objects.count()
    new_posts = Post.objects.order_by('-time')[:10]
    
    return_data = {
        'post_num' : postNum,
        'new_posts' : [],
    }

    for i in new_posts:
        return_data['new_posts'].append({
            'post_id': i.post_id,
            'uid' : i.uid.uid,
            'uname' : i.uid.uname,
            'gender' : i.uid.gender,
            'avatar' : '/media/'+i.uid.avatar.name,
            'title' : i.title,
            'type' : i.type,
            'text' : i.text[:50],
            'time' : i.time.strftime("%Y-%m-%d %H:%M:%S"),
            'like_num' : i.like_num,
        })

    return returnList(return_data)

def getPost(request,pid):
    post_obj = Post.objects.filter(post_id=pid).first()

    if not post_obj:
        return return403('无此文章')
    if pid<=0:
        return return403('参数非法')

    comments = Comment.objects.filter(post_id=pid)

    return_data = {
        'post_id': post_obj.post_id,
        'uid' : post_obj.uid.uid,
        'uname' : post_obj.uid.uname,
        'gender' : post_obj.uid.gender,
        'avatar' : '/media/'+post_obj.uid.avatar.name,
        'title' : post_obj.title,
        'text' : post_obj.text,
        'type' : post_obj.type,
        'cover' : post_obj.cover,
        'time' : post_obj.time.strftime("%Y-%m-%d %H:%M:%S"),
        'like_num' : post_obj.like_num,
        'comment_num' : comments.count(),
        'comments' : []
    }

    
    for i in comments:
        return_data['comments'].append({
            'comment_id': i.comment_id,
            'uid' : i.uid.uid,
            'uname' : i.uid.uname,
            'gender' : post_obj.uid.gender,
            'avatar' : '/media/'+i.uid.avatar.name,
            'text' : i.text,
            'time' : i.time.strftime("%Y-%m-%d %H:%M:%S"),
            'like_num' : i.like_num,
        })


    return returnList(return_data)

def getPage(request,page_num):
    page_obj = Post.objects.order_by('-time')[(page_num-1)*10:page_num*10] 

    return_data = {
        'page_num' : page_num,
        'post_num' : page_obj.count(),
        'posts' : []
    }
    for i in page_obj:
        return_data['posts'].append({
            'post_id': i.post_id,
            'uid' : i.uid.uid,
            'uname' : i.uid.uname,
            'gender' : i.uid.gender,
            'avatar' : '/media/'+i.uid.avatar.name,
            'title' : i.title,
            'type' : i.type,
            'cover' : i.cover,
            'text' : i.text[:50],
            'time' : i.time.strftime("%Y-%m-%d %H:%M:%S"),
            'like_num' : i.like_num,
        })
    
    return returnList(return_data)

def newPost(request):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    title = request.POST.get("title")
    text = request.POST.get("text")
    type = request.POST.get("type")
    if not (title and text and type):
        return return403('参数无效')
    uid_obj=User.objects.filter(uid=uid).first()
    post_obj=Post(uid=uid_obj,title=title,type=type,text=text,time=datetime.now())
    post_obj.save()
    return return200('操作成功')

def editPost(request,pid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    title = request.POST.get("title")
    text = request.POST.get("text")
    if not (pid and title and text):
        return return403('参数无效')
    post_obj = Post.objects.filter(post_id=pid,uid=uid).first()
    if not post_obj:
        return return403('只有作者可以修改文章')
    
    post_obj.title=title
    post_obj.text=text
    post_obj.save()
    return return200('操作成功')


def deletePost(request,pid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    post_obj = Post.objects.filter(post_id=pid,uid=uid).first()
    if not post_obj:
        return return403('找不到文章')
    
    post_obj.delete()
    return return200('操作成功')


def likePost(request,pid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    post_obj = Post.objects.filter(post_id=pid).first()
    if not post_obj:
        return return403('找不到文章')
    
    like_mark = request.session.get('p'+str(pid),None)
    if like_mark:
        return return403('已经点过赞啦~')
    
    post_obj.like_num = post_obj.like_num + 1
    post_obj.save()

    request.session['p'+str(pid)] = 1
    return return200('操作成功')

def newComment(request):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    pid = request.POST.get("post_id")
    text = request.POST.get("text")
    if not (pid and text):
        return return403('参数无效')
    uid_obj = User.objects.filter(uid=uid).first()
    pid_obj = Post.objects.filter(post_id=pid).first()
    if not pid_obj:
        return return403('找不到文章')
    comment_obj = Comment(uid=uid_obj,post_id=pid_obj, text=text,time=timezone.now())
    comment_obj.save()
    return return200('操作成功')

def deleteComment(request,cid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    comment_obj = Comment.objects.filter(comment_id=cid,uid=uid).first()
    if not comment_obj:
        return return403('找不到评论')
    
    comment_obj.delete()
    return return200('操作成功')


def likeComment(request,cid):
    uid=request.session.get('uid',None)
    if not uid:
        return return403('未登录或登录超时')
    comment_obj = Comment.objects.filter(comment_id=cid).first()
    if not comment_obj:
        return return403('找不到评论')
    
    like_mark = request.session.get('c'+str(cid),None)
    if like_mark:
        return return403('已经点过赞啦~')
    
    comment_obj.like_num = comment_obj.like_num + 1
    comment_obj.save()

    request.session['c'+str(cid)] = 1
    return return200('操作成功')
