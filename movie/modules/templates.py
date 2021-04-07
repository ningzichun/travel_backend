from moviepy.editor import *
from .resources import *

total_photo_template=[1,2,3,3,4]

def openning_simple(title = "Title", desc = '',bg_image=randImage()):
    default_font=randFont()
    title_clip = TextClip(title.encode('utf-8'), color='white', font=default_font, kerning=5, fontsize=100).set_duration(8).set_start(crossTime).crossfadein(0.8).set_pos(('center',450))
    line_clip = TextClip('-----------------------------------', color='white', fontsize=50, font=default_font,size=screensize).set_duration(6).set_pos(('center',90)).set_start(1.2+crossTime).crossfadein(1)
    desc_clip = TextClip(desc, color='white', fontsize=50, font=default_font,size=screensize).set_duration(6).set_pos(('center',170)).set_start(1.2+crossTime).crossfadein(1)
    openning_background_image_clip = ImageClip(np.array(cut_to_cover(bg_image)))
    openning = CompositeVideoClip([openning_background_image_clip,line_clip,title_clip,desc_clip], size=screensize).subclip(0, 5)
    return (openning,5)

def photo_one_simple(images,bg_image=None):
    cut_image = np.array(generate_background_image(images[0]))
    background_clip = ImageClip(cut_image,duration=6)
    front_clip = ImageClip(images[0],duration=8).resize(width=2112, height=1188).set_pos(lambda t: ('center', 0-50+int((0.9*t*t-11*t+38))))
    clips_i = [background_clip,front_clip]
    #this_part = CompositeVideoClip(clips_i,size=screensize)
    return (clips_i,5)

def photo_two_simple(images,bg_image=randImage()):
    background_clip = ImageClip(np.array(cut_to_cover(bg_image)))
    clip1 = ImageClip(images[0],duration=10).resize(width=1300, height=750).set_start(crossTime).add_mask().rotate(3).set_pos(lambda t: (120+t,100+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(images[1],duration=8).resize(width=1300, height=750).set_start(crossTime+3).add_mask().rotate(358).set_pos(lambda t: (540, 120+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2]
    return (part_clips,9)


def photo_three_simple(images,bg_image=randImage()):
    background_clip = ImageClip(np.array(cut_to_cover(bg_image)))
    clip1 = ImageClip(images[0],duration=10).resize(width=1200, height=490).set_start(crossTime).add_mask().rotate(5).set_pos(lambda t: (120+t,150+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(images[1],duration=8).resize(width=1200, height=490).set_start(crossTime+2.5).add_mask().rotate(353).set_pos(lambda t: (980, 90+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip3 = ImageClip(images[2],duration=8).resize(width=1200, height=490).set_start(crossTime+5.5).add_mask().rotate(10).set_pos(lambda t: (540+t, 450+2*t)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2,clip3]
    #this_part = CompositeVideoClip(part_clips,size=screensize)
    return (part_clips,9)

def photo_three_1(images,bg_image=""):
    background_clip = ImageClip(templates_path+'temp_31.png')
    clip1 = ImageClip(np.array(cut_to_size(1216 ,624,images[0])),duration=10).set_start(crossTime).add_mask().set_pos((28 ,15 )).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_to_size(702 ,354,images[1])),duration=8).set_start(crossTime+2.5).add_mask().set_pos((26 , 670 )).crossfadein(0.5).crossfadeout(0.5)
    clip3 = ImageClip(np.array(cut_to_size(498 ,359,images[2])),duration=8).set_start(crossTime+5.5).add_mask().set_pos((1301 , 15 )).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2,clip3]
    return (part_clips,9)

def photo_four_1(images,bg_image=""):
    background_clip = ImageClip(templates_path+'temp_41.png')
    clip1 = ImageClip(np.array(cut_to_size(709,402,images[0])),duration=10).set_start(crossTime).add_mask().set_pos((196,103)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(np.array(cut_to_size(709,402,images[1])),duration=8).set_start(crossTime+2.5).add_mask().set_pos((958, 139)).crossfadein(0.5).crossfadeout(0.5)
    clip3 = ImageClip(np.array(cut_to_size(709,402,images[2])),duration=8).set_start(crossTime+5.5).add_mask().set_pos((198, 539)).crossfadein(0.5).crossfadeout(0.5)
    clip4 = ImageClip(np.array(cut_to_size(709,402,images[2])),duration=8).set_start(crossTime+5.5).add_mask().set_pos((958, 573)).crossfadein(0.5).crossfadeout(0.5)
    part_clips = [background_clip,clip1,clip2,clip3,clip4]
    return (part_clips,9)

def photo_one_with_poem_simple(images,bg_image=randImage(),poem="层楼倚高阁\n走马拥江东\n欲问升平日\n交交第二功"):
    background_clip = ImageClip(np.array(cut_to_cover(bg_image)))
    clip1 = ImageClip(images[0],duration=10).resize(width=1200, height=600).set_start(crossTime).add_mask().rotate(3).set_pos(lambda t: (130+t,200+2*t)).crossfadein(0.5).crossfadeout(0.5)
    text_clip = TextClip(poem, color='white', fontsize=80, font=randPoemFont(),size=screensize).set_duration(10).set_pos(lambda t: (500+t,0)).set_start(2).crossfadein(1)
    part_clips = [background_clip,clip1,text_clip]
    this_part = CompositeVideoClip(part_clips,size=screensize)
    return (this_part,8)

def photo_two_with_poem_simple(images,bg_image=randImage(),poem="层楼倚高阁\n走马拥江东\n欲问升平日\n交交第二功"):
    background_clip = ImageClip(np.array(cut_to_cover(bg_image)))
    clip1 = ImageClip(images[0],duration=12).resize(width=900, height=400).set_start(crossTime).add_mask().rotate(3).set_pos(lambda t: (50+t,150+2*t)).crossfadein(0.5).crossfadeout(0.5)
    clip2 = ImageClip(images[1],duration=10).resize(width=900, height=400).set_start(crossTime+2).add_mask().rotate(359).set_pos(lambda t: (450+t,500+2*t)).crossfadein(0.5).crossfadeout(0.5)
    text_clip = TextClip(poem, color='white', fontsize=88, font=randPoemFont(),size=screensize).set_duration(10).set_pos(lambda t: (490+t,0)).set_start(3).crossfadein(1.5)
    part_clips = [background_clip,clip1,clip2,text_clip]
    this_part = CompositeVideoClip(part_clips,size=screensize)
    return (this_part,9)

def ending_simple(text = "END",bg_image=randImage()):
    circle_mask = VideoFileClip(masks_path+'circle_open_center.mov',has_mask=True).to_mask()
    ending = TextClip(text, color='white', fontsize=50, kerning=5,interline=2, font=randFont(),bg_color='#555',size=screensize).set_duration(6)
    ending_clip = CompositeVideoClip([ending], size=screensize).subclip(0, 5)
    return (ending_clip,5)


openning_templates = [
    openning_simple
]

photo_templates = [
    photo_one_simple,
    photo_two_simple,
    photo_three_simple,
    photo_three_1,
    photo_four_1
]

photo_with_poem_templates = [
    photo_one_with_poem_simple,
    photo_two_with_poem_simple
]

ending_templates = [
    ending_simple
]

