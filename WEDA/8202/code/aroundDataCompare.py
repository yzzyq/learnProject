import numpy as np
import math

def getAroundData(data_index, allPoistion, threshold):
    lenPoistion = len(allPoistion)
    # 记录相互靠近的光谱
    aroundData = []
    allPoistion = np.array(allPoistion)
    for this_pos in range(lenPoistion):
        if data_index != this_pos:
            dis = math.sqrt(sum(pow(allPoistion[this_pos,:] - allPoistion[data_index,:],2)))
            if dis < threshold:
                aroundData.append(this_pos)
    return aroundData



# 周边数据的比较
# def getAroundData(allPoistion,threshold):
#     lenPoistion = len(allPoistion)
#     # 记录相互靠近的光谱
#     aroundData = []

#     for this_pos in range(lenPoistion):
#         NegPoistion = []
#         # 找出所有邻近的点
#         for other_pos in range(lenPoistion):
#             if this_pos != other_pos:
#                 dis = math.sqrt(sum(pow(np.array(allPoistion[this_pos]) - np.array(allPoistion[other_pos]),2)))
#                 if dis < threshold:
#                     NegPoistion.append(other_pos)
#         aroundData.append(NegPoistion)
#     # updateAroundData(dataProcess,aroundData)  
#     return aroundData

# 根据周围的类别更新数据的类别
def updateAroundData(dataProcess,aroundData):
    lenData = len(dataProcess)
    for i in range(lenData):
        num = 0
        for j in aroundData[i]:
            if dataProcess[j,-1] == 1:
                num += dataProcess[j,-1]
        if num > 0:
            num = num // 5 + 1
            num = num / 10
        dataProcess[i,2] = num


