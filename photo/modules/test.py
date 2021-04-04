from PIL import Image
import random
# 测试
img1=Image.open("lenna_bicubic_x3.bmp")
img2=Image.open("butterfly_GT_bicubic_x3.bmp")

img2=img2.convert('RGBA')
img2=img2.rotate(30,expand=1)
r,g,b,a = img2.split()
img1.paste(img2, (50, 50),mask=a)
img1=img1.rotate(30)
img1.show()
