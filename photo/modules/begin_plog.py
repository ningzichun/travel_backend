from PIL import Image, ImageDraw, ImageFont
from . import pl_lunzi as lz
KuaileFontPath = './photo/modules/resources/Kuaile.ttf'
font = ImageFont.truetype(KuaileFontPath, 24)

bg_image = './photo/modules/resources/background.png'

def add_text_to_image(image, text, font=font):
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)
    # 设置文本颜色和透明度
    image_draw.text(text_xy, text, font=font, fill=(76, 234, 124, 180))

    image_with_text = Image.alpha_composite(rgba_image, text_overlay)

    return image_with_text


def get_end(poem = "层楼倚高阁\n走马拥江东\n欲问升平日\n交交第二功"):
    back=Image.open("./photo/modules/imgs/2.png")
    backgroud = lz.add_text(back, KuaileFontPath, [76, 234, 124, 180], 240, poem,
                            [900, 800])
    return backgroud
def get_begin(city_image_path):
    back=Image.open(bg_image)
    im_before = Image.open(city_image_path)# 该城市的风景照片
    im_rgb = Image.new("RGB", im_before.size, (255, 255, 255))
    im_rgb.paste(im_before, mask=im_before.split()[3]) # 3 is the alpha channel
    
    im2 = Image.open("./photo/modules/imgs/1.png")
    backgroud = im2
    back.resize((im2.width,im2.height))
    im2 = im2.convert('RGBA')
    r, g, b, a = im2.split()

    lz.add_pic(backgroud, im_rgb, [38, 1363, 2958, 3302])

    backgroud.paste(im2, (0, 0), mask=a)
    backgroud = lz.add_text(backgroud, KuaileFontPath, [76, 234, 124, 180], 240, "Travle log", [1685, 3848])
    back.paste(backgroud,(0,0))
    #backgroud.show()
    return backgroud
