from moviepy.editor import *
from .resources import *


# 开头
def openning_simple(title = "Title", desc = '',bg_image=randImage()):
    default_font=randFont()
    title_clip = TextClip(title.encode('utf-8'), color='white', font=default_font, stroke_width=0.5,stroke_color='#222222',kerning=5, font_size=140).with_duration(8).with_start(crossTime).crossfadein(3).with_position(('center',400))
    line_clip = TextClip('-----------------------------------', color='white', font_size=50, font=default_font,size=screensize).with_duration(6).with_position(('center',90)).with_start(1.2+crossTime).crossfadein(1)
    desc_clip = TextClip(desc, color='white', font_size=50, font=default_font,size=screensize).with_duration(6).with_position(('center',170)).with_start(1.2+crossTime).crossfadein(1)
    openning_background_image_clip = ImageClip(np.array(cut_to_cover(bg_image)))
    openning = CompositeVideoClip([openning_background_image_clip,line_clip,title_clip,desc_clip], size=screensize).subclip(0, 5).add_mask()
    openning.write_videofile("op.mp4",fps=5)
    return (openning,5)

def openning_title_photo_1(title = "Title", desc = '',bg_image=randImage()):
    default_font=randFont()
    if len(title)>5:
        font_size = 70
    font_size = 130
    title_clip = TextClip(title.encode('utf-8'), color='#7f7f7f', font=default_font,kerning=1, font_size=font_size,size=((615,1080))).with_position((1305,-200)).with_duration(8).with_start(crossTime).crossfadein(0.8)
    desc_clip = TextClip(desc, color='#7f7f7f', font_size=50, font=default_font,size=((615,1080))).with_duration(6).with_position((1305,-50)).with_start(0.5+crossTime).crossfadein(1)
    footer_clip = TextClip("PHOTO ALBUM", color='#222222', font_size=20, font=default_font,size=((615,1080))).with_duration(6).with_position((1305,500)).with_start(0.5+crossTime).crossfadein(1)
    color_clip = ColorClip(size=screensize,color=(223, 234, 240)).with_duration(12)
    openning_background_image_clip = ImageClip(np.array(cut_to_size(1305 ,1080,bg_image)),duration=10).with_position((0,0))
    openning = CompositeVideoClip([color_clip,footer_clip,openning_background_image_clip,title_clip,desc_clip], size=screensize).subclip(0, 5)
    return (openning,5)

def openning_title_photo_2(title = "Title", desc = '',bg_image=randImage()):
    default_font=randFont()
    if len(title)>5:
        font_size = 70
    font_size = 130
    title_clip = TextClip(title.encode('utf-8'), color='#7f7f7f', font=default_font,kerning=1, font_size=font_size,size=((615,1080))).with_position((0,-200)).with_duration(8).with_start(crossTime).crossfadein(0.8)
    desc_clip = TextClip(desc, color='#7f7f7f', font_size=50, font=default_font,size=((615,1080))).with_duration(6).with_position((0,-50)).with_start(0.5+crossTime).crossfadein(1)
    footer_clip = TextClip("PHOTO ALBUM", color='#222222', font_size=20, font=default_font,size=((615,1080))).with_duration(6).with_position((0,500)).with_start(0.5+crossTime).crossfadein(1)
    color_clip = ColorClip(size=screensize,color=(223, 234, 240)).with_duration(12)
    openning_background_image_clip = ImageClip(np.array(cut_to_size(1305 ,1080,bg_image)),duration=10).with_position((615,0))
    openning = CompositeVideoClip([color_clip,footer_clip,openning_background_image_clip,title_clip,desc_clip], size=screensize).subclip(0, 5)
    return (openning,5)


# 简约型
def photo_one_simple(images):
    cut_image = np.array(generate_background_image(images[0]))
    background_clip = ImageClip(cut_image,duration=6)
    front_clip = ImageClip(images[0],duration=8).resize(width=2112, height=1188).with_position(lambda t: ('center', 0-50+int((0.9*t*t-11*t+38))))
    clips_i = [background_clip,front_clip]
    return (clips_i,5)

def photo_two_simple_winter(images):
    bg_image=randWinter()
    background_clip = ImageClip(np.array(cut_to_cover(bg_image)))
    clip1 = ImageClip(np.array(cut_with_border(1300,750,images[0])),duration=10).with_start(crossTime).add_mask().rotate(3).with_position(lambda t: (120+t,100+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_with_border(1300,750,images[1])),duration=10).with_start(crossTime+3).add_mask().rotate(358).with_position(lambda t: (540, 120+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2]
    return (part_clips,9)

def photo_two_simple_rainy(images):
    bg_image=randRainy()
    background_clip = ImageClip(np.array(cut_to_cover(bg_image)))
    clip1 = ImageClip(np.array(cut_with_border(1300,750,images[0])),duration=10).with_start(crossTime).add_mask().rotate(2.8).with_position(lambda t: (115+t,110+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_with_border(1300,750,images[1])),duration=10).with_start(crossTime+3).add_mask().rotate(358.2).with_position(lambda t: (530, 115+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2]
    return (part_clips,9)

def photo_three_simple_sunny(images):
    bg_image = randSunny()
    background_clip = ImageClip(np.array(cut_to_cover(bg_image)))
    clip1 = ImageClip(np.array(limit_hw_border(668,501,images[0])),duration=10).with_start(crossTime).add_mask().rotate(4).with_position(lambda t: (120+t,150+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(limit_hw_border(668,501,images[1])),duration=10).with_start(crossTime+2.5).add_mask().rotate(356).with_position(lambda t: (980, 90+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip3 = ImageClip(np.array(limit_hw_border(668,501,images[2])),duration=10).with_start(crossTime+5.5).add_mask().rotate(3).with_position(lambda t: (540+t, 450+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2,clip3]
    return (part_clips,9)

# 背景相关类
def photo_three_1(images):
    background_clip = ImageClip(images_path+'temp_31.png')
    clip1 = ImageClip(np.array(cut_with_border(1216 ,624,images[0])),transparent=True,duration=10).with_start(crossTime).add_mask().with_position((28 ,15 )).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_with_border(702 ,354,images[1])),transparent=True,duration=8).with_start(crossTime+2.0).add_mask().with_position((26 , 670 )).crossfadein(0.5).crossfadeout(0.5)
    clip3 = ImageClip(np.array(cut_with_border(498 ,359,images[2])),transparent=True,duration=8).with_start(crossTime+3.5).add_mask().with_position((1301 , 15 )).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2,clip3]
    return (part_clips,9)

def photo_three_rect(images):
    background_clip = ImageClip(images_path+'rect.png')
    clip1 = ImageClip(np.array(cut_with_border(753 ,502,images[0])),transparent=True,duration=10).with_start(crossTime).add_mask().with_position((200,176)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_with_border(586 ,391,images[1])),transparent=True,duration=8).with_start(crossTime+2.5).add_mask().with_position((1078,118)).crossfadein(0.5).crossfadeout(0.5)
    clip3 = ImageClip(np.array(cut_with_border(601 ,401,images[2])),transparent=True,duration=8).with_start(crossTime+4).add_mask().with_position((902,544)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2,clip3]
    return (part_clips,9)

def photo_four_1(images):
    background_clip = ImageClip(images_path+'temp_41.png')
    clip1 = ImageClip(np.array(cut_with_border(709,402,images[0])),duration=10).with_start(crossTime).add_mask().with_position((196,103)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_with_border(709,402,images[1])),duration=8).with_start(crossTime+2.5).add_mask().with_position((958, 139)).crossfadein(0.5).crossfadeout(0.5)
    clip3 = ImageClip(np.array(cut_with_border(709,402,images[2])),duration=8).with_start(crossTime+5.2).add_mask().with_position((198, 539)).crossfadein(0.5).crossfadeout(0.5)
    clip4 = ImageClip(np.array(cut_with_border(709,402,images[3])),duration=8).with_start(crossTime+5.2).add_mask().with_position((958, 573)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2,clip3,clip4]
    return (part_clips,9)

def photo_four_maitian(images):
    background_clip = ImageClip(images_path+'maitian.png')
    clip1 = ImageClip(np.array(cut_with_border(660,450,images[0])),transparent=True,duration=10).with_start(crossTime).add_mask().rotate(0.03).with_position((397,104)).crossfadein(0.5)
    clip2 = ImageClip(np.array(cut_with_border(620,465,images[1])),transparent=True,duration=8).with_start(crossTime+2.5).add_mask().rotate(6.81).with_position((1076, 61)).crossfadein(0.5)
    clip3 = ImageClip(np.array(cut_with_border(560,420,images[2])),transparent=True,duration=8).with_start(crossTime+5).add_mask().rotate(5.75).with_position((434, 509)).crossfadein(0.5)
    clip4 = ImageClip(np.array(cut_with_border(588,441,images[3])),transparent=True,duration=8).with_start(crossTime+5.5).add_mask().rotate(356.14).with_position((1133, 509)).crossfadein(0.5)
    part_clips = [background_clip,clip1,clip2,clip3,clip4]
    return (part_clips,9)

# 长图类
def photo_long_three_autumn(images):
    background_clip = ImageClip(images_path+'autumn.png')#2652
    clip1 = ImageClip(np.array(cut_with_border(752,564,images[0])),duration=10).with_start(crossTime).add_mask().rotate(1.15).with_position((1242,464)).crossfadein(0.5)
    clip2 = ImageClip(np.array(cut_with_border(720,540,images[1])),duration=8).with_start(crossTime+2.5).add_mask().rotate(358.6).with_position((713, 28)).crossfadein(0.5)
    clip3 = ImageClip(np.array(cut_with_border(752,564,images[2])),duration=8).with_start(crossTime+4.5).add_mask().rotate(358.6).with_position((65, 471)).crossfadein(0.5)
    part_clips = [background_clip,clip1,clip2,clip3]
    long_part = CompositeVideoClip(part_clips,size=(3456,1080)).add_mask()
    part_clips2 = [long_part.with_position(lambda t: (-672,0) if t<0.5 else((-768+192*t,0) if t<4 else (0,0)))]
    return (part_clips2,8)


def photo_long_four_raing(images):
    background_clip = ImageClip(images_path+'raing.png')
    clip1 = ImageClip(np.array(cut_with_border(690,518,images[0])),duration=10).with_start(crossTime).add_mask().rotate(3).with_position((2537,447)).crossfadein(0.5)
    clip2 = ImageClip(np.array(cut_with_border(690,518,images[1])),duration=8).with_start(crossTime+2.5).add_mask().rotate(358).with_position((1759, 508)).crossfadein(0.5)
    clip3 = ImageClip(np.array(cut_with_border(690,518,images[2])),duration=8).with_start(crossTime+4.5).add_mask().rotate(359).with_position((990, 44)).crossfadein(0.5)
    clip4 = ImageClip(np.array(cut_with_border(690,518,images[3])),duration=8).with_start(crossTime+5.5).add_mask().rotate(357.9).with_position((631, 457)).crossfadein(0.5)
    part_clips = [background_clip,clip1,clip2,clip3,clip4]
    long_part = CompositeVideoClip(part_clips,size=(3456,1080)).add_mask()
    #long_part.write_videofile("aaa.mp4",fps=2)
    part_clips2 = [long_part.with_position(lambda t: (-1536,0) if t<2 else((-1920+192*t,0) if t<9 else (-192,0)))]
    return (part_clips2,11)

# 视频背景类
def photo_two_video_rainy(images):
    background_clip = VideoFileClip(get_bg_video("rainy")).with_duration(9)
    clip1 = ImageClip(np.array(cut_with_border(1300,750,images[0])),duration=10).with_start(crossTime).add_mask().rotate(3).with_position(lambda t: (120+t,100+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_with_border(1300,750,images[1])),duration=10).with_start(crossTime+3).add_mask().rotate(358).with_position(lambda t: (540, 120+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2]
    return (part_clips,9)

def photo_two_video_snow(images):
    background_clip = VideoFileClip(get_bg_video("snow")).with_duration(9)
    clip1 = ImageClip(np.array(cut_with_border(1300,750,images[0])),duration=10).with_start(crossTime).add_mask().rotate(3).with_position(lambda t: (120+t,100+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_with_border(1300,750,images[1])),duration=10).with_start(crossTime+3).add_mask().rotate(358).with_position(lambda t: (540, 120+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2]
    return (part_clips,9)

def photo_two_video_sunny(images):
    background_clip = VideoFileClip(get_bg_video("sunny")).with_duration(9)
    clip1 = ImageClip(np.array(cut_with_border(1300,750,images[0])),duration=10).with_start(crossTime).add_mask().rotate(3).with_position(lambda t: (120+t,100+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_with_border(1300,750,images[1])),duration=10).with_start(crossTime+3).add_mask().rotate(358).with_position(lambda t: (540, 120+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2]
    return (part_clips,9)

def photo_three_video_snow(images):
    background_clip = VideoFileClip(get_bg_video('snow')).with_duration(9)
    clip1 = ImageClip(np.array(cut_with_border(752,564,images[0])),duration=10).with_start(crossTime).add_mask().rotate(1.15).with_position((1050,464)).crossfadein(0.5)
    clip2 = ImageClip(np.array(cut_with_border(720,540,images[1])),duration=8).with_start(crossTime+1.5).add_mask().rotate(358.6).with_position((713, 28)).crossfadein(0.5)
    clip3 = ImageClip(np.array(cut_with_border(752,564,images[2])),duration=8).with_start(crossTime+3.5).add_mask().rotate(358.6).with_position((130, 480)).crossfadein(0.5)
    part_clips = [background_clip,clip1,clip2,clip3]
    return (part_clips,8)

def photo_three_video_sunny(images):
    background_clip = VideoFileClip(get_bg_video('sunny')).with_duration(9)
    clip1 = ImageClip(np.array(cut_with_border(752,564,images[0])),duration=10).with_start(crossTime).add_mask().rotate(1.15).with_position((1050,464)).crossfadein(0.5)
    clip2 = ImageClip(np.array(cut_with_border(720,540,images[1])),duration=8).with_start(crossTime+1.5).add_mask().rotate(358.6).with_position((713, 28)).crossfadein(0.5)
    clip3 = ImageClip(np.array(cut_with_border(752,564,images[2])),duration=8).with_start(crossTime+3.5).add_mask().rotate(358.6).with_position((135, 480)).crossfadein(0.5)
    part_clips = [background_clip,clip1,clip2,clip3]
    return (part_clips,8)

def photo_three_video_rainy(images):
    background_clip = VideoFileClip(get_bg_video('rainy')).with_duration(9)
    clip1 = ImageClip(np.array(cut_with_border(752,564,images[0])),duration=10).with_start(crossTime).add_mask().rotate(1.15).with_position((1050,464)).crossfadein(0.5)
    clip2 = ImageClip(np.array(cut_with_border(720,540,images[1])),duration=8).with_start(crossTime+1.5).add_mask().rotate(358.6).with_position((713, 28)).crossfadein(0.5)
    clip3 = ImageClip(np.array(cut_with_border(752,564,images[2])),duration=8).with_start(crossTime+3.5).add_mask().rotate(358.6).with_position((138, 480)).crossfadein(0.5)
    part_clips = [background_clip,clip1,clip2,clip3]
    return (part_clips,8)

# 前景类
def photo_one_m1(images):
    color_clip = ColorClip(size=(1920,1080),color=(223, 234, 240),duration=8)
    background_clip = ImageClip(np.array(cut_to_size(1920,1080,images[0])),duration=7).add_mask().resize(width = lambda t:2000+300*t if t<1 else(2100+200*t if t<1.5 else 2400)).rotate(lambda t:350+10*t if t<1 else 0).with_position('center')
    front_clip = VideoFileClip(images_path+'mask1.gif', has_mask=True).with_duration(6.5)
    part_clips = [color_clip,background_clip,front_clip]
    return (part_clips,6.5)

def photo_one_f1(images):
    color_clip = ColorClip(size=(1920,1080),color=(223, 234, 240),duration=8)
    background_clip = ImageClip(np.array(cut_to_size(1920,1080,images[0])),duration=6).add_mask().resize(width = lambda t:2620-280*t if t<2 else 2060).rotate(lambda t:345+15*t  if t<1 else 0).with_position('center')
    front_clip = VideoFileClip(images_path+'front1.gif', has_mask=True).with_duration(6)
    part_clips = [color_clip,background_clip,front_clip]
    return (part_clips,5.8)

def photo_one_f2(images):
    color_clip = ColorClip(size=(1920,1080),color=(223, 234, 240),duration=8)
    background_clip = ImageClip(np.array(cut_to_size(1920,1080,images[0])),duration=6).add_mask().resize(width = lambda t:2620-280*t if t<2 else 2060).rotate(lambda t:12.5-12.5*t  if t<1 else 0).with_position('center')
    front_clip = VideoFileClip(images_path+'front2.gif', has_mask=True).with_duration(6)
    part_clips = [color_clip,background_clip,front_clip]
    return (part_clips,5.8)



# 诗词



def poem_w_1(images, text="层楼倚高阁\n走马拥江东\n欲问升平日\n交交第二功"):
    lines = text.split('\n')
    for line in range(4):
        lines[line]=lines[line]+('，'if line%2==0 else '。')
    font = randPoemFont()
    background_clip = ImageClip(np.array(cut_to_size(1920,1080,randPoemBg())),duration=9).add_mask()
    poem_line1 = TextClip(lines[0], color='black', font_size=100, font=font,size=screensize).with_duration(10).with_position((450,-260)).with_start(0.5).crossfadein(1)
    poem_line2 = TextClip(lines[1], color='black', font_size=100, font=font,size=screensize).with_duration(10).with_position((452,-130)).with_start(1).crossfadein(1)
    poem_line3 = TextClip(lines[2], color='black', font_size=100, font=font,size=screensize).with_duration(10).with_position((450,10)).with_start(2).crossfadein(1)
    poem_line4 = TextClip(lines[3], color='black', font_size=100, font=font,size=screensize).with_duration(10).with_position((450,140)).with_start(2.5).crossfadein(1)
    clip1 = ImageClip(np.array(cut_with_border(800,600,images[0])),duration=10).with_start(0.5).add_mask().rotate(3).with_position(lambda t: (130+t,200+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,poem_line1,poem_line2,poem_line3,poem_line4]
    this_part = CompositeVideoClip(part_clips,size=screensize).with_duration(8)
    return (this_part,8)

def poem_w_2(images,text="层楼倚高阁\n走马拥江东\n欲问升平日\n交交第二功"):
    lines = text.split('\n')
    for line in range(4):
        lines[line]=lines[line]+('，'if line%2==0 else '。')
    background_clip = ImageClip(np.array(cut_to_size(1920,1080,randPoemBg())),duration=9).add_mask()
    font = randPoemFont()
    poem_line1 = TextClip(lines[0], color='black', font_size=100, font=font,size=screensize).with_duration(10).with_position((-450,-260)).with_start(0.5).crossfadein(1)
    poem_line2 = TextClip(lines[1], color='black', font_size=100, font=font,size=screensize).with_duration(10).with_position((-450,-130)).with_start(1).crossfadein(1)
    poem_line3 = TextClip(lines[2], color='black', font_size=100, font=font,size=screensize).with_duration(10).with_position((-450,10)).with_start(2).crossfadein(1)
    poem_line4 = TextClip(lines[3], color='black', font_size=100, font=font,size=screensize).with_duration(10).with_position((-450,140)).with_start(2.5).crossfadein(1)

    clip1 = ImageClip(np.array(cut_with_border(800,600,images[0])),duration=10).with_start(0.5).add_mask().rotate(1.5).with_position(lambda t: (900+t,220+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,poem_line1,poem_line2,poem_line3,poem_line4]
    this_part = CompositeVideoClip(part_clips,size=screensize).with_duration(8)
    return (this_part,8)

def poem_h_1(images,text="层楼倚高阁\n走马拥江东\n欲问升平日\n交交第二功"):
    lines=["","","","",""]
    t = text.split('\n')
    for line in range(4):
        for ch in t[line]:
            lines[line]=lines[line]+ch+'\n'
    background_clip = ImageClip(np.array(cut_to_size(1920,1080,randPoemBg())),duration=9).add_mask()
    font = randPoemFont()
    clip1 = ImageClip(images[0],duration=6).add_mask().resize(width = lambda t:2000+300*t if t<1 else(2100+200*t if t<2 else 2500)).rotate(lambda t:335+15*t if t<1 else(340+10*t if t<2 else 0)).with_position('center')

    poem_line1 = TextClip(lines[0], color='black', font_size=80, font=font,size=screensize).with_duration(10).with_position((660,-25)).with_start(0.5).crossfadein(1)
    poem_line2 = TextClip(lines[1], color='black', font_size=80, font=font,size=screensize).with_duration(10).with_position((540,15)).with_start(1).crossfadein(1)
    poem_line3 = TextClip(lines[2], color='black', font_size=80, font=font,size=screensize).with_duration(10).with_position((420,55)).with_start(2.3).crossfadein(1)
    poem_line4 = TextClip(lines[3], color='black', font_size=80, font=font,size=screensize).with_duration(10).with_position((300,95)).with_start(2.8).crossfadein(1)

    clip1 = ImageClip(np.array(cut_with_border(800,600,images[0])),duration=10).with_start(0.5).add_mask().rotate(1).with_position(lambda t: (130+t,200+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,poem_line1,poem_line2,poem_line3,poem_line4]
    this_part = CompositeVideoClip(part_clips,size=screensize).with_duration(8)
    return (this_part,8)

def photo_two_with_poem_simple(images,poem="层楼倚高阁\n走马拥江东\n欲问升平日\n交交第二功"):
    background_clip = ImageClip(np.array(cut_to_cover(randPoemBg())))
    clip1 = ImageClip(images[0],duration=12).resize(width=900, height=400).with_start(crossTime).add_mask().rotate(3).with_position(lambda t: (50+t,150+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(images[1],duration=10).resize(width=900, height=400).with_start(crossTime+2).add_mask().rotate(359).with_position(lambda t: (450+t,500+2*t)).crossfadein(0.5).crossfadeout(0.5)
    text_clip = TextClip(poem, color='white', font_size=88, font=randPoemFont(),stroke_width=1.5,stroke_color='#323232',size=screensize).with_duration(10).with_position(lambda t: (490+t,0)).with_start(3).crossfadein(1.5)
    part_clips = [background_clip,clip1,clip2,text_clip]
    this_part = CompositeVideoClip(part_clips,size=screensize)
    return (this_part,9)
    

def ending_simple(text = "END"):
    ending = TextClip(text, color='white', font_size=50, kerning=5,interline=2, font=randFont(),bg_color='#555',size=screensize).with_duration(6)
    ending_clip = CompositeVideoClip([ending], size=screensize).subclip(0, 5)
    return (ending_clip,5)

def ending_1(text = "END"):
    ending = VideoFileClip(images_path+'end1.mp4')
    this_part = CompositeVideoClip([ending],size=screensize).with_duration(8)
    return (this_part,8)

openning_templates = [
    openning_simple,
    openning_title_photo_1,
    openning_title_photo_2
]

total_photo_template=[
    2,2,3,3,3,4,4,3,4,2,2,2,3,3,3,1,1,1,1
]


photo_templates = [
    photo_two_simple_winter,
    photo_two_simple_rainy,
    photo_three_simple_sunny,
    photo_three_1,
    photo_three_rect,
    photo_four_1,
    photo_four_maitian,
    photo_long_three_autumn,
    photo_long_four_raing,
    photo_two_video_rainy,
    photo_two_video_snow,
    photo_two_video_sunny,
    photo_three_video_snow,
    photo_three_video_sunny,
    photo_three_video_rainy,
    photo_one_m1,
    photo_one_f1,
    photo_one_f2,
    photo_one_simple,
]
#0'多云', 1'雨', 2'雪', 3'晴', 4'中性'
photo_templates_weather = [
    2,1,3,4,4,4,3,3,1,1,2,3,2,3,1,4,4,4,4
]
photo_templates_color = [
    [54,150,250],
    [96,131,169],
    [251,255,220],
    [210,237,255],
    [221,219,209],
    [193,237,219],
    [254,240,195],
    [250,243,203],
    [218,233,230],
    [41,79,53],
    [194,201,217],
    [255,235,189],
    [143,148,162],
    [178,160,132],
    [41,79,53],
    [252,255,227],
    [215,162,20],
    [215,162,20],
    [215,162,20],
]

photo_with_poem_templates = [
    poem_w_1,
    poem_w_2,
    poem_h_1
]

ending_templates = [
    ending_simple,
    ending_1
]

transitions = [
    "windowslice",
    "BowTieVertical",
    "BowTieHorizontal",
    "WaterDrop",
    "InvertedPageCurl",
    "PolkaDotsCurtain",
    "luminance_melt",
    "Dreamy",
    "crosshatch",
    "Radial",
    "angular",
    "circleopen",
    "cube",
    "directionalwipe",
    "doorway",
    "randomsquares",
    'squareswire',
    'swap',
    'wind',
    'InvertedPageCurl',
    'InvertedPageCurl',
]
def randOpenning():
    return random.sample(openning_templates,1)[0]

def randTrans():
    return random.sample(transitions,1)[0]

def randDura():
    return random.randint(500,1000)
