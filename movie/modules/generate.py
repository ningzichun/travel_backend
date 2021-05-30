from moviepy.editor import *
from .resources import *
from .templates import *
import billiard as multiprocessing

multi_files = []

def genClipByCommand(type,comm,target_fps):
    print(type,comm)
    coverGen = 0
    if type==1:
        openning,op_duration = openning_templates[comm['id']](comm['title'],comm['desc'],comm['bg_image'])
        if random.random()>0.6:
            coverGen = 1
            np_frame = openning.get_frame(op_duration-1)
            generateCover(np_frame,comm['cover'])   #生成封面
        return exportTmpFile(openning.with_duration(op_duration),target_fps)
    elif type==2:
        this_clips, clip_duration = photo_templates[comm['id']](comm['images'])
        if(comm['gif_num']):
            gif_num = comm['gif_num']
            gifs = comm['gifs']
            for i in range(gif_num):
                this_clips.append(VideoFileClip(gifs[i]["path"], has_mask=True).resize(height=gifs[i]['size']).with_fps(target_fps).freeze(total_duration=clip_duration).with_start(0).with_position((gifs[i]['position'][0], gifs[i]['position'][1])))
        result_clip = CompositeVideoClip(this_clips,size=screensize).with_duration(clip_duration)
        if not coverGen:
            coverGen = 1
            np_frame = result_clip.get_frame(clip_duration-1)
            generateCover(np_frame,comm['cover'])   #生成封面
        return exportTmpFile(result_clip,target_fps)
    elif type==3:
        this_clip, clip_duration = photo_with_poem_templates[comm['id']](comm['images'],comm['poem'])
        return exportTmpFile(this_clip.with_duration(clip_duration),target_fps)
    elif type==5:
        ending, ed_duration = ending_templates[comm['id']](comm['text'])
        return exportTmpFile(ending.with_duration(ed_duration),target_fps)

def concatClips(tmp_files,result_file,music_clip):
    target_comm = { "videos":[], "transitions":[],'args':['-shortest','-pix_fmt','yuv420p'],'concurrency':10 }
    target_comm['output'] = result_file
    target_comm['audio'] = music_clip
    for i in tmp_files:
        target_comm["videos"].append(i)
    for i in range(len(tmp_files)-1):
        target_comm["transitions"].append({
            "name" : randTrans(),
            "duration" : randDura()
        })
    target_comm = "module.paths.push('/usr/local/lib/node_modules/'); const concat = require('ffmpeg-concat'); concat(" + str(target_comm) + ")"
    with open(result_file+".js", 'w') as output_file:
        output_file.write(target_comm)
    cmd = 'xvfb-run -s "-ac -screen 0 1280x1024x24" node '+result_file+".js"
    print(cmd)
    print(target_comm)
    return not os.system(cmd)


def error_handler(e):
    raise Exception(str(e))

def generateMovie(command):
    cover_name = command['openning']['cover']
    print(command)

    pool = multiprocessing.Pool(processes=16)
    workers=[]
    current_time=0
    target_fps = command['fps']

    print("开头生成")
    workers.append(pool.apply_async(genClipByCommand,(1,command['openning'],target_fps),error_callback=error_handler))

    
    print("展览片段生成")
    templates = command['middle']['templates']
    for i in range(command['middle']['num']):
        templates[i]['cover'] = cover_name
        print(templates[i])
        workers.append(pool.apply_async(genClipByCommand,(2,templates[i],target_fps),error_callback=error_handler))
    
    if 'poem' in command:
        print("诗词片段生成")
        templates = command['poem']['templates']
        for i in range(command['poem']['num']):
            print(templates[i])
            workers.append(pool.apply_async(genClipByCommand,(3,templates[i],target_fps),error_callback=error_handler))
    
    print("结尾生成")
    workers.append(pool.apply_async(genClipByCommand,(5,command['ending'],target_fps),error_callback=error_handler))
    
    pool.close()

    print("等待片段合成...")
    
    tmp_files = []
    for i in workers:
        filename = i.get()
        if filename:
            tmp_files.append(filename)
            print(filename,"片段完成")
    print("所有片段",tmp_files)

    pool.join()
    
    #写文件
    print("合成序列")
    # multi_files = tmp_files
    if not concatClips(tmp_files,command['location'],command['music']):
        raise Exception("合成序列失败")
    
    #清理文件
    
    import os
    for i in tmp_files:
        if os.path.exists(i):
            os.remove(i)
    return True


