from moviepy.editor import *
import moviepy.video.fx.all as vfx
from .resources import *
from .templates import *
import billiard as multiprocessing
#from moviepy.multithreading import multithread_write_videofile

multi_files = []
music_clip = None
def genClipByCommand(type,comm):
    print(type,comm)
    if type==1:
        openning,op_duration = openning_templates[comm['id']](comm['title'],comm['desc'],comm['bg_image'])
        #openning.save_frame(comm['cover'], t='00:00:04')
        np_frame = openning.get_frame(op_duration-1)
        generateCover(np_frame,comm['cover'])   #生成封面
        return exportTmpFile(openning.set_duration(op_duration))
    elif type==2:
        this_clips, clip_duration = photo_templates[comm['id']](comm['images'],comm['bg_image'])
        if(comm['gif_num']):
            gif_num = comm['gif_num']
            gifs = comm['gifs']
            for i in range(gif_num):
                print(gifs[i])
                this_clips.append(VideoFileClip(gifs[i]["path"], has_mask=True).resize(height=gifs[i]['size']).set_fps(5).set_duration(8).set_start(0).set_position((gifs[i]['position'][0], gifs[i]['position'][1])))
        return exportTmpFile(CompositeVideoClip(this_clips,size=screensize).set_duration(clip_duration))
    elif type==3:
        this_clip, clip_duration = photo_with_poem_templates[comm['id']](comm['images'],comm['bg_image'],comm['poem'])
        return exportTmpFile(this_clip.set_duration(clip_duration))
    elif type==5:
        ending, ed_duration = ending_templates[comm['id']](comm['text'],comm['bg_image'])
        return exportTmpFile(ending.set_duration(ed_duration))


def generateMovie(command):

    print(command)

    pool = multiprocessing.Pool(processes=10)
    workers=[]
    current_time=0

    print("开头生成")
    print(command['openning'])
    workers.append(pool.apply_async(genClipByCommand,(1,command['openning'])))

    
    print("展览片段生成")
    print(command['middle'])
    templates = command['middle']['templates']
    for i in range(command['middle']['num']):
        print(templates[i])
        workers.append(pool.apply_async(genClipByCommand,(2,templates[i])))
    

    if 'poem' in command:
        print("诗词片段生成")
        print(command['poem'])
        templates = command['poem']['templates']
        for i in range(command['poem']['num']):
            print(templates[i])
            workers.append(pool.apply_async(genClipByCommand,(3,templates[i])))
    

    print("结尾生成")
    print(command['ending'])
    workers.append(pool.apply_async(genClipByCommand,(5,command['ending'])))
    
    pool.close()

    #音乐
    global multi_files
    global music_clip

    print("音乐预处理")
    music_clip = AudioFileClip(command['music'])

    print("等待片段合成...")
    
    tmp_files = []
    tmp_clips = []
    for i in workers:
        filename = i.get()
        if filename:
            tmp_files.append(filename)
            print(filename)
            print(tmp_files)
            tmp_clips.append(VideoFileClip(filename).crossfadein(1))

    pool.join()
    
    #写文件
    multi_files = tmp_files
    print("合成序列")
    final_clip = concatenate(tmp_clips,padding=-1, method="compose")
    audio_clip = afx.audio_loop( music_clip, duration=final_clip.duration)
    final_clip = final_clip.set_audio(audio_clip)
    final_clip.write_videofile(command['location'],fps=command['fps'])

    #清理文件
    
    import os
    for i in tmp_files:
        if os.path.exists(i):
            os.remove(i)
    return final_clip

def generateCompose():
    global multi_files
    tmp_clips = []
    for i in multi_files:
            tmp_clips.append(VideoFileClip(i).crossfadein(1))
    final_clip = concatenate(tmp_clips,padding=-1, method="compose")
    audio_clip = afx.audio_loop( music_clip, duration=final_clip.duration)
    final_clip = final_clip.set_audio(audio_clip)
    return final_clip

def generateMovieMultithread(Incommand):
    global command 
    command = Incommand
    multithread_write_videofile('multi.mp4',generateCompose,moviepy_threads=5,ffmpeg_threads=1,fps=5)

