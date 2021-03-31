# Create your tasks here

from celery import shared_task
from movie.models import Work
from time import sleep
from django.utils import timezone
import traceback
import json
import random


from travel.resources.cn_dict import cn_dict


@shared_task
def makeMovie(wid,uid):
    #default_retry_delay=300, max_retries=5
    str_wid = str(wid)
    work_dir = "./media/movies/"+str(wid)
    print(work_dir)
    print(str_wid+": 开始生成")
    work_obj = Work.objects.filter(work_id = wid).first()
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

        work_obj.status_msg = "正在生成影集"
        work_obj.save()

        
        # 生成诗词
        work_obj.status = 103
        work_obj.status_msg = "正在生成诗词"
        work_obj.save()
        from travel.load_files import generatePoet

        img0_fac = load_dict['factors'][0]
        keyword = weather_specises[weather[0]]+" "+cn_dict[img0_fac["types"][2]]
        if(img0_fac["values"][1]>0.1):
            keyword = keyword+" "+cn_dict[img0_fac["types"][1]]
        res_poem = ""

        for i in range(5):
            result = generatePoet(keyword,5,1,0)
            if result:
                res_poem = result
                break

        # 模板匹配
        work_obj.status = 104
        work_obj.status_msg = "正在匹配模板"
        work_obj.save()
        from movie.modules.genetic import FromHere
        command = FromHere(img_num,image_paths,weather,color,load_dict,res_poem)

        # 组装命令
        vid_name = "/result"+randStr(4)+".mp4"
        cov_name = "/cover"+randStr(4)+".jpg"
        command['location'] = work_dir+vid_name
        command['openning']['cover'] = work_dir+cov_name

        # 影集生成
        work_obj.status = 105
        work_obj.status_msg = "正在生成影集"
        work_obj.save()
        from movie.modules.generate import generateMovie
        generateMovie(command)
        
        
        work_obj = Work.objects.filter(work_id = wid).first()
        work_obj.status = 200 #处理完成
        work_obj.status_msg = "处理完成"
        work_obj.result_msg = "/media/movies/"+str(wid)+vid_name
        work_obj.movie_cover = "/media/movies/"+str(wid)+cov_name
        work_obj.save()

        # 分享影集
        from movie.views import shareMovie
        if 'share' in load_dict:
            if load_dict['share']:
                movie_info = {
                    'work_id': i.work_id,
                    'movie_title' : i.movie_title,
                    'movie_description' : i.movie_description,
                    'movie_cover' : i.movie_cover,
                    'create_time' : i.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'update_time' : i.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'status' : i.status,
                    'status_msg' : i.status_msg,
                    'result_msg' : i.result_msg,
                }
                shareMovie(uid,movie_info)
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
