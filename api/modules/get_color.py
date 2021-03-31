#!/usr/bin/python
# coding=utf-8
import cv2
import numpy as np
import random
from numpy import *

#数据流入函数
def loadDataSet(imageFile):
    fileNPArray = np.frombuffer(imageFile, np.uint8)
    img = cv2.imdecode(fileNPArray ,cv2.IMREAD_COLOR)
    #img=cv2.imread(imageFile)
    dataMat = [];
    for line in img:
        for color_obj in line:
            dataMat.append(color_obj);
    return dataMat

# 计算欧几里得距离
def distEclud(vecA, vecB):
#    return sqrt(sum(power(vecA - vecB, 2))) # 求两个向量之间的距离
    distance=0;
    num=len(vecA)
   # print(">>");
    #print(num);
    for i in range(0,num,1):

        distance+=(vecA[i]-vecB[i])*(vecA[i]-vecB[i]);
    return  sqrt(distance)


# 构建聚簇中心，取k个(此例中为4)随机质心
def randCent(dataSet, k):
    #n = shape(dataSet)[1]
    centroids=[];
    len_dataset=len(dataSet);
    for j in range(0,k,1):
        while True:
           # print("P");
            ok=0;
            p=random.randint(0,len_dataset);
            obj_centroids=dataSet[p];
            num=len(centroids);
            #print("helo")
            #print(obj_centroids);
            #print("F")
            for k in range(0,num,1):
                #print("yes");
                #print(centroids[k]);
                the_center=centroids[k];
                if all(the_center==obj_centroids):
                    ok=1;
            if ok==0:
                centroids.append(obj_centroids);
                break;
    return centroids

# k-means 聚类算法
def kMeans(dataSet, k):

    nums = len(dataSet);
    diffs=zeros(nums);
    myCentroids=randCent(dataSet,k);

    #print("is");
    #print(myCentroids);
    times=1000;#最大迭代次数
    min_d=0.001;#阈值;
    time=0;

    print(nums);

    while time<times:
       # print("P")
        new_center=[];

        #确定所属的类：

        for i in range(0,nums,1):
           # print("x")
            distance=10000000;#超级大的值，冷启动。
            diff=0;
            for j in range(0,k,1):
                num_distance=distEclud(myCentroids[j],dataSet[i]);
                if(num_distance<distance):
                    distance=num_distance;
                    diffs[i]=j;

        #更新聚簇中心
        for j in range(0,k,1):
          #  print("yesok")
           # print(myCentroids);
            number=0;
            r=0;
            g=0;
            b=0;
            for i in range(0,nums,1):
                if(diffs[i]==j):
                    r+=dataSet[i][0];
                    g+=dataSet[i][1];
                    b+=dataSet[i][2];
                    number=number+1;

            obj_r=r/number;
            obj_g=g/number;
            obj_b=b/number;
            obj_center=[obj_r,obj_g,obj_b];
            new_center.append(obj_center);

        d=0;
        for i in range(0,k,1):
            d+=distEclud(myCentroids[i],new_center[i]);
        myCentroids=new_center;
        if d<min_d:
            break;
        time=time+1;
    return myCentroids;


# --------------------测试and接口------------------------
def getColor(imageFile,k=3):
    # 用测试数据及测试kmeans算法
    datMat = loadDataSet(imageFile)
    my_center=kMeans(datMat,k)

    return(my_center)

    #返回数据格式：  [[b,g,r],[b,g,r]...]  //k个三维向量 因为写反了所以顺序是 b g r
