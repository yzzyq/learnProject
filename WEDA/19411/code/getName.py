import os
import numpy as np

# def getFileNameByIndex(index, file_name):
#     true_name = []
#     write_file = '3611-10-50.txt'
#     process_index = list(map(lambda x : x - 1, index))
#     print(list(process_index))
#     for one_index in process_index:
#         print(one_index)
#         one_file_name = file_name[one_index]
#         with open(write_file, 'a') as f:
#             f.write(str(one_file_name) + '\n')

# if __name__ == '__main__':
#     index = [1602, 1630, 1156, 744, 175, 13, 67, 202, 1148, 1143, 1858, 14, 1009, 1769, 29, 1052, 39, 1273, 62, 615, 1799, 
#     144, 100, 1323, 645, 1145, 114, 1613, 680, 1190, 1062, 157, 203, 779, 1083, 1431, 1671, 1407, 758, 1352]
#     file_name = os.listdir('3000-4000/10-50')
#     getFileNameByIndex(index, file_name)


"""
Created on Sun Nov 03 21:26:44 2019

@author: 86182
"""

#k-means聚类支持函数
# from numpy import *
# #将文本文件导入到一个列表中，该返回值是一个包含许多其他列表的列表，这种格式很容易将很多值封装到矩阵中
# def loadDataSet(filename):
# #dataMat=np.loadtxt('C:\\my_project\\testSet.txt')
#     dataMat= []
#     fr =open(filename)
#     for line in fr.readlines():
#         curLine = line.strip().split('\t')
#         fltLine = map(float,curLine)
#         dataMat.append(fltLine)
#     return dataMat

# #计算两个向量的欧氏距离
# def distEclud(vecA,vecB):
#     return sqrt(sum(power(vecA-vecB,2)))
# #该函数可以为给定数据集构建一个包含k个随机质心的集合

# def randCent(dataSet,k):
#     n= shape(dataSet)[1]
#     print(n)
#     centroids = mat(zeros((k,n)))
#     for j in range(n):
#         minJ = min(dataSet[:,j])
#         rangeJ = float(max(dataSet[:,J])-minJ)
#         centroids[:,j] = minJ +rangeJ * random.rand(k,l)
#     return centorids
# #k-means 聚类算法

# def kMeans(dataSet, k, distMeans=distEclud, createCent = randCent):
#     m = shape(dataSet)[0]
#     clusterAssment = mat(zeros((m,2)))    
#     #用于存放该样本属于哪类及质心距离
#     #clusterAssment第一列存放该数据所属的中心点，第二列是该数据到中心点的距离
#     centroids = createCent(dataSet, k)
#     clusterChanged = True   
#     #用来判断聚类是否已经收敛
#     while clusterChanged:
#         clusterChanged = False
#         for i in range(m):  
#             #把每一个数据点划分到离它最近的中心点
#             minDist = inf; minIndex = -1
#             for j in range(k):
#                 distJI = distMeas(centroids[j,:], dataSet[i,:])
#                 if distJI < minDist:
#                     minDist = distJI; minIndex = j  
#                     #如果第i个数据点到第j个中心点更近，则将i归属为j
#             if clusterAssment[i,0] != minIndex: clusterChanged = True;  # 如果分配发生变化，则需要继续迭代
#             clusterAssment[i,:] = minIndex,minDist**2   
#             #并将第i个数据点的分配情况存入字典
#         # print centroids
#         for cent in range(k):   
#             #重新计算中心点
#             ptsInClust = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]   # 去第一列等于cent的所有列
#             centroids[cent,:] = mean(ptsInClust, axis = 0) 
#             #算出这些数据的中心点
#     return centroids, clusterAssment

if __name__ == '__main__':
    np.set_printoptions(suppress = True)
    a = [[74, 973.5502503065248, -716.7323910121767], [98, 532.5123035393842, -485.9205593570415], [0, 11708717.52063442, -172194.85313790845], 
    [127, 489.53768376698366, -301.79147572436773], [4, 211382.9111753244, -110335.93054032545], [8, 12322.519445267024, -11813.219272861623], 
    [197, 74.54685834253438, -62.84275867130293], [20, 5829.77785924687, -3877.5623391052436], [23, 3811.41879649978, -3610.980322831665], 
    [51, 1623.5095320549815, -1258.242730874408]]

    print(a)
    b = np.array(a)
    print(b)
    


