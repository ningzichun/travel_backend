# Create your tasks here

from celery import shared_task
from photo.models import Photo
from time import sleep
from django.utils import timezone
import traceback
import json
import random
import os

from travel.resources.cn_dict import cn_dict
from travel.modules.location import coordinate2image
from PIL import Image, ImageDraw, ImageFont


@shared_task

def makePhoto(wid,uid):
    str_wid = str(wid)
    work_dir = "./media/photos/"+str(wid)
    work_dir1=work_dir+"/"  #存显著性矩阵的临时文件夹
    print(work_dir)
    print(str_wid+": 开始生成")
    photo_obj = Photo.objects.filter(work_id = wid).first()
    try:
        photo_obj.status = 101
        photo_obj.status_msg = "正在分析命令参数"
        photo_obj.save()
        print("正在分析命令参数")

        # 读取info 处理path 传递参数
        with open( work_dir + "/info.json",'r') as load_f:
            load_dict = json.load(load_f)
        images_in_json = list(load_dict["images"])
        image_paths = [ work_dir+"/"+i for i in images_in_json]
        print(image_paths)
        img_num = len(images_in_json)   


        # 图像识别
        photo_obj.status = 102
        photo_obj.status_msg = "正在分析图片"
        photo_obj.save()
        print("正在分析图片颜色天气信息")

        ## 天气识别
        from movie.modules.info import getInfo

        weather_specises = ['云', '雨', '雪', '晴']
        weather,color = getInfo(image_paths)

        ## 城市印象图
        if (('latitude' not in load_dict) or ('longitude' not in load_dict)):
            city_image = coordinate2image(None,None)
        else:
            print(load_dict['latitude'],load_dict['longitude'])
            city_image = coordinate2image(load_dict['latitude'],load_dict['longitude'])
        print("印象图匹配",city_image)

        # 生成诗词
        photo_obj.status = 103
        photo_obj.status_msg = "正在生成诗词"
        photo_obj.save()
        print("正在生成诗词")
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

        print(res_poem)
        # 显著性检测
        photo_obj.status = 104
        photo_obj.status_msg = "正在进行显著性检测"
        photo_obj.save()
        from photo.modules.PoolNet import caijian_main as cm
        
        image_path1=[i for i in images_in_json]
        image_path_final=[]
            #图片resize
        for pic_name in image_path1:
            img = Image.open(work_dir+'/'+pic_name)
            k = img.width / 150
            img1 = img.resize((int(img.width / k), int(img.height / k)))
            img1.save(work_dir1+'linshi'+pic_name)
            image_path_final.append("linshi" +pic_name)

        print(image_path1)
        print(work_dir1)

        print(image_path_final)
        cm.get_cv(work_dir1,image_path_final)
        for pic_name in image_path1:
            os.remove(work_dir1 + 'linshi'+pic_name)


        # 组装命令
        res_name = "/photo"+randStr(4)+".jpg"
        cov_name = "/cover"+randStr(4)+".jpg"

        # 长图生成
        photo_obj.status = 105
        photo_obj.status_msg = "正在生成长图"
        photo_obj.save()
        from photo.modules.genetic_for_longpic import generatePhoto
        cover_width,cover_height,res_width,res_height = generatePhoto(img_num,image_paths,weather,color,work_dir+cov_name,work_dir+res_name,work_dir1,city_image,res_poem)
        
        
        photo_obj.status = 200 #处理完成
        photo_obj.status_msg = "处理完成"
        photo_obj.result_msg = "/media/photos/"+str(wid)+res_name
        photo_obj.photo_cover = "/media/photos/"+str(wid)+cov_name
        photo_obj.cover_width = cover_width
        photo_obj.cover_height = cover_height
        photo_obj.photo_width = res_width
        photo_obj.photo_height = res_height

        photo_obj.save()

        print("Finish.")
    except Exception as e:
        print(traceback.format_exc(e))
        photo_obj.status = -1 #失败
        photo_obj.status_msg = "生成失败："+repr(e)
        print(str_wid+": 生成失败")
        photo_obj.save()
        return False

    print(str_wid+": 结束生成")
    return True


def randStr(length = 4):
    num_set = [chr(i) for i in range(48,58)]
    char_set = [chr(i) for i in range(97,123)]
    total_set = num_set + char_set
    result_set = "".join(random.sample(total_set, length))
    return result_set
