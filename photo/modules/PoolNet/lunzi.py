from PIL import Image, ImageDraw, ImageFont
import cv2
#显著性检测的box
def get_box(img):
    # src=[[0 ,0 ,0 ,0 ,0, 0, 0],
    #      [0, 0, 1, 0, 0, 0, 0],
    #      [0, 0, 1, 0, 0, 0, 0],
    #      [0, 0, 1, 1, 0, 1, 0],
    #      [0, 0, 0, 1, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0],
    #      ]
    # height=8
    # weight=7
    src = img
    height = src.shape[0]
    weight = src.shape[1]
    up = 0
    down = height
    left = 0
    right = weight
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)#灰度化处理
    src = cv2.threshold(src, 127, 1, cv2.THRESH_BINARY)
   # dst = cv2.adaptiveThreshold(src, 102, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 1)#二值化
    print(src[1])
    ok = 0
    tx = 0
    file_handle = open('1.txt', mode='w')
    for i in range(height):
        for j in range(weight):
            if src[1][i][j]==0:
                file_handle.write(" ")
            else:
                file_handle.write("*")
        file_handle.write("\n")


    # 找到矩形的left 和 right
    #
    # print(src)
    # 找到矩形up和down：
    for i in range(height):
        pre_tx = tx
        tx = 0
        for j in range(weight):
            tx = tx + src[1][i][j]
        if i!=1:
            if up==0 and pre_tx == 0 and tx != 0:
                up = i
            elif down==height and pre_tx != 0 and tx == 0:
                down = i
    # 找到矩形的left 和 right

    tx = 0
    for i in range(weight):
        pre_tx = tx
        tx = 0
        for j in range(height):
            tx = tx + src[1][j][i]
        if i != 1:
            if left==0 and pre_tx == 0 and tx != 0:
                left = i
            elif right==weight and pre_tx != 0 and tx == 0:
                right = i



    box=[up,down,left,right]
    return box

def getposition(img,box,weight,height):

    w=img.width
    h=img.height
    # w=150
    # h=400
    h_middle=(box[0]+box[1])/2

    w_middle=(box[2]+box[3])/2
    h_middle=200
    w_middle=150
    wls=w/weight
    hls=h/height
    print(wls)
    print(hls)
    if wls>hls:
        print("1")
        w2=weight*hls
        print(w2)
        h2=height*hls
        print(hls)
        left=0
        right=0
        up =0
        down=h2
        if w_middle < w2/2:
            left=0
            right=w2
        elif w_middle > w-w2/2:
            left=w-w2
            right=w
        else:
            left=w_middle-w2/2
            right=w_middle+w2/2
        box=[up/hls,down/hls,left/hls,right/hls,hls]
        return box
    else:

        w2=weight*wls
        h2=height*wls
        up=0
        down=0
        left=0
        right=w2
        print("right")
        print(right)
        if h_middle < h2 / 2:
            up = 0
            down = h2
        elif h_middle > h-h2/2:
            up = h - h2
            down = h
        else:
            up = h_middle - h2 / 2
            down = h_middle + h2 / 2
        box = [up / wls, down / wls, left / wls, right / wls,wls]
        return box

