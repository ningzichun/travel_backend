from celery import shared_task
from photo.models import Photo
from time import sleep
from django.utils import timezone
import traceback
import json
import random


@shared_task
def makePhoto(wid,uid):
    str_wid = str(wid)
    work_dir = "./media/photos/"+str(wid)
    print(work_dir)
    print(str_wid+": 开始生成")
    work_obj = Photo.objects.filter(work_id = wid).first()
    try:
        work_obj.status = 101
        work_obj.status_msg = "正在分析命令参数"
        work_obj.save()

        # 读取info 处理path 传递参数
        with open( work_dir + "/info.json",'r') as load_f:
            load_dict = json.load(load_f)
        images_in_json = list(load_dict["images"])
        image_paths = [ work_dir+"/"+i for i in images_in_json]
        print(image_paths)
        img_num = len(images_in_json)

        # 图像识别
        work_obj.status = 102
        work_obj.status_msg = "正在分析图片"
        work_obj.save()
        from movie.modules.info import getInfo

        weather_specises = ['云', '雨', '雪', '晴']
        weather,color = getInfo(image_paths)
        
        # 组装命令
        res_name = "/result"+randStr(4)+".png"
        cov_name = "/cover"+randStr(4)+".jpg"
        command['location'] = work_dir+res_name

        # 长图生成
        work_obj.status = 105
        work_obj.status_msg = "正在生成长图"
        work_obj.save()
        from photo.modules.generate import get_long_picture
        get_long_picture(command)
        
        
        work_obj = Photo.objects.filter(work_id = wid).first()
        work_obj.status = 200 #处理完成
        work_obj.status_msg = "处理完成"
        work_obj.result_msg = "/media/photos/"+str(wid)+res_name
        work_obj.photo_cover = "/media/photos/"+str(wid)+cov_name
        work_obj.save()

        # 分享长图
        from photo.views import shareFunc
        if 'share' in load_dict:
            if load_dict['share']:
                photo_info = {
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
                shareFunc(uid,photo_info)
        print("Finish.")
    except Exception as e:
        print(traceback.format_exc(e))
        work_obj.status = -1 #失败
        work_obj.status_msg = "生成失败："+repr(e)
        print(str_wid+": 生成失败")
        work_obj.save()
        return False
        #self.retry(e)

    print(str_wid+": 结束生成")
    return True

def randStr(length = 4):
    num_set = [chr(i) for i in range(48,58)]
    char_set = [chr(i) for i in range(97,123)]
    total_set = num_set + char_set
    result_set = "".join(random.sample(total_set, length))
    return result_set
