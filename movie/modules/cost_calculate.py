#为遗传算法提供计算代价函数的方法
#
#import synonyms as sy
import math
color_weight=1
factor_weight=1
weather_weight=1


#主题色的计算,容易理解
def color(rgb_a,rgb_b):
    #print("rgb")
    #print(math.sqrt((rgb_a[0]-rgb_b[0])*(rgb_a[0]-rgb_b[0])+(rgb_a[1]-rgb_b[1])*(rgb_a[1]-rgb_b[1])+(rgb_a[2]-rgb_b[2])*(rgb_a[2]-rgb_b[2]))-20000)
    return math.sqrt((rgb_a[0]-rgb_b[0])*(rgb_a[0]-rgb_b[0])+(rgb_a[1]-rgb_b[1])*(rgb_a[1]-rgb_b[1])+(rgb_a[2]-rgb_b[2])*(rgb_a[2]-rgb_b[2]))-200

#关键词之间的计算
def factor(factor_a,factor_b):
#    return sy.compare(factor_a,factor_b,seg=True)
    return 0
#天气
def weather(weather_a,weather_b):
    if weather_a==weather_b:
        return -100
    else:
        #print("weather")
        #print((weather_a-weather_b)*(weather_a-weather_b))
        return (weather_a-weather_b)*(weather_a-weather_b)

def chongfu(selfs):
    ts=0
    for i in range(0,len(selfs.path)):
        for j in range(0,len(selfs.path)):
            if i!=j:
                if selfs.path[i]==selfs.path[i]:
                    ts+=5
    return ts
