import selfDataCompare as sdc
import numpy as np



#选择的元素有Hb、NII、NII、SII、SII
#查看线性表中的发射线的情况
def getOtherEmissionLine(dataSet,dataProcess,side):
    all_Centers = [6549,6585,6718,6732]
    i = 0
    sideLen = 2*side + 1
    #每条数据的处理
    for data in dataSet:
        all_Trust = []
        all_goodline = []
        for center in all_Centers:
            # print('center:',center)
            trust,is_goodLine = getOneValue(data,sideLen,center)
            all_Trust.append(trust)
            all_goodline.append(is_goodLine)
        # print('all_goodline:',all_goodline)
        # print('all_Trust:',all_Trust)
        high_confidence = np.where(np.array(all_Trust[:]) > 1.1)[0]
        # high_confidence = list(map(lambda x:x+1,high_confidence))
        if len(high_confidence) >= 2 or \
            (len(high_confidence) == 1 and \
                [all_goodline[index] for index in range(len(all_goodline)) if index not in high_confidence].count(1) >= 1):
            # all_goodline[1:].count(1) >= 2:
            for index,trust in enumerate(all_Trust):
                if trust > 1.5:
                    all_Trust[index] += all_Trust[index]
            dataProcess[i,1] = sum(all_Trust)

        if all_goodline[:].count(1) >= 2:
            temp_value = [all_Trust[index] for index in range(len(all_goodline)) if all_goodline[index]]
            dataProcess[i,1] += sum(temp_value)*2

        if isMeet(all_goodline, all_Trust):
            if dataProcess[i,0] < 1:
                dataProcess[i,1] = 0
                dataProcess[i,-1] = -1
        i += 1


        

# def isMeet(all_goodline, all_Trust):
#     meet = False
#     if all_goodline.count(1) + [one_trust < 1.1 for one_trust in all_Trust].count(0) < 2:
#         meet = True
#     if all_goodline.count(1) == 1 and [one_trust < 1.1 for one_trust in all_Trust].count(0) == 1:
#         if all_Trust[all_goodline.index(1)] > 1.1:
#             meet = True
#     return meet


# def getOneValue(data,sideLen,center):
#     peak_value = []
#     before_slope = None
#     isMout = False
#     ispadd_2754 = False
#     # isMout_middle = False
#     isSpecial = False
#     ispadd_4310 = False
#     ispadd_4310_tall = 0
#     mout_value = []
#     len_data = len(data[0])
#     value = 0
#     min_value = float('inf')
#     trust = 0
#     is_goodLine = 0
#     # slope_value = 0
#     if data[0][-1] > center+(sideLen-1)//2:
#         for i in range(len_data):
#             if center-(sideLen-1)//2 <= data[0][i] <= center+(sideLen-1)//2:
#                 if min_value > data[1][i]:
#                     min_value = data[1][i]
#                 value = data[1][i+1]
#                 #需要记录峰值
#                 slope = (data[1][i+1] - data[1][i])/(data[0][i+1] - data[0][i])
#                 #距离边缘值
#                 if before_slope == None:
#                     peak_value.append(data[1][i])
#                 else:
#                     if before_slope > 0 and slope < 0:
#                         #如果是6564附近的值，需要记录下来
#                         if center-2 < data[0][i] < center+2:
#                             is_special = False
#                             if center - 1 < data[0][i] < center + 1 and abs(before_slope) <= 0.02:
#                                 if (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0.1:
#                                     is_special = True
#                             if center - 1 < data[0][i] < center + 1 and abs(slope) <= 0.03:
#                                 if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < -0.1:
#                                     is_special = True

#                             #分为好几种情况
#                             # print(abs(before_slope),abs(slope))
#                             if (abs(before_slope) > 0.02 and abs(slope) > 0.03) or is_special:

#                                 if center + 1 < data[0][i] < center + 2:
#                                     if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
#                                        (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2]) < 0.4:
#                                         isMout = False
#                                         break

#                                     if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                        ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
#                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
#                                        (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-2]) < 0.4:
#                                         isMout = False
#                                         break
                                    
#                                     if ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
#                                         ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
#                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
#                                        (data[1][i-1] - data[1][i-3]) / (data[1][i] - data[1][i-1]) < 0.7:
#                                         isMout = False
#                                         break

#                                 # print('第一个检查')
#                                 if center-2 < data[0][i] < center - 1:
#                                     if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
#                                         (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 0.4:
#                                         isMout = False
#                                         break

#                                     if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                         ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
#                                         (data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+2]) < 0.4:
#                                         if (data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]) > 0.1:
#                                             isMout = False
#                                             break
                                    
#                                     if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
#                                         ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
#                                         (data[1][i+1] - data[1][i]) / (data[1][i+2] - data[1][i+1]) < 0.1:
#                                         isMout = False
#                                         break 
                                    
#                                     if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                         ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
#                                         ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
#                                         ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) < 0 and \
#                                         (data[1][i] - data[1][i-3]) / (data[1][i] - data[1][i+3]) < 0.4:
#                                         isMout = False
#                                         break

#                                     if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                         ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
#                                         ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
#                                         ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
#                                         (data[1][i] - data[1][i-3]) / (data[1][i] - data[1][i+2]) < 1.2:
#                                         isMout = False
#                                         break

#                                     if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                         ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
#                                         ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) > 0 and \
#                                         ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) < 0 and \
#                                         ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
#                                         (data[1][i] - data[1][i-4]) / (data[1][i] - data[1][i+2]) < 1.2:
#                                         isMout = False
#                                         break
                                    
#                                     if (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                         ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) > 0 and \
#                                         ((data[1][i-4] - data[1][i-3])/(data[0][i-4] - data[0][i-3])) > 0 and \
#                                         ((data[1][i-5] - data[1][i-4])/(data[0][i-5] - data[0][i-4])) < 0 and \
#                                         ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
#                                         (data[1][i] - data[1][i-4]) / (data[1][i] - data[1][i+2]) < 0.4:
#                                         isMout = False
#                                         break
                                    
#                                     isMout = True
#                                     mout_value.append(data[1][i])
#                                 # print('第二个检查')    
#                                 if center - 1 < data[0][i] < center + 2:
#                                     if center - 1 < data[0][i] < center:
#                                         if ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
#                                             ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
#                                             ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                             ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0 and \
#                                             ((data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4])) > 0 and \
#                                             ((data[1][i-4] - data[1][i-5])/(data[0][i-4] - data[0][i-5])) > 0 and \
#                                             ((data[1][i-5] - data[1][i-6])/(data[0][i-5] - data[0][i-6])) > 0 and \
#                                             ((data[1][i-6] - data[1][i-7])/(data[0][i-6] - data[0][i-7])) < 0 and \
#                                             0.9 < ((data[1][i] - data[1][i-6]) / (data[1][i] - data[1][i+2])) < 1.2:
#                                             isMout = False
#                                             break

#                                     if center < data[0][i] < center + 1 and \
#                                        ((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+1])) < 0.1 and \
#                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
#                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0:
#                                         isMout = False
#                                         break
                                    
#                                     # 12000中的0-10的1278的特殊情况
#                                     # print((data[1][i+3] - data[1][i+2]) / (data[1][i] - data[1][i+1]))
#                                     # print((data[1][i] - data[1][i+4]) / (data[1][i] - data[1][i-1]))
#                                     if center < data[0][i] < center + 1 and \
#                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
#                                         ((data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2])) > 0 and \
#                                         ((data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3])) < 0 and \
#                                         ((data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4])) > 0 and \
#                                         ((data[1][i+3] - data[1][i+2]) / (data[1][i] - data[1][i+1])) < 0.02 and \
#                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
#                                         0.8 < ((data[1][i] - data[1][i+4]) / (data[1][i] - data[1][i-1])) < 1.2:
#                                         isMout = False
#                                         break
                                    


#                                     if center < data[0][i] < center + 1 and \
#                                        ((data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+1])) < 0.1 and \
#                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) > 0 and \
#                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) > 0 and \
#                                        ((data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3])) < 0:
#                                         isMout = False
#                                         break

#                                     if center < data[0][i] < center + 1 and \
#                                        ((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1])) < 0 and \
#                                        ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0 and \
#                                        ((data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2])) < 0.15:
#                                     #    ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2])) < 0:
#                                         isMout = False
#                                         # print('2')
#                                         break

#                                     isMout = True
#                                     # isMout_middle = True
#                                     mout_value.append(data[1][i])
#                                     if center < data[0][i] < center + 1 and \
#                                        0.5 < (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+1]) < 2 and \
#                                        (((data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]))* \
#                                         ((data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]))) < 0:
#                                     #    0.8 < abs(before_slope / slope) < 1.2 and \
#                                         is_goodLine = 1

#                                     # 俩边差不多长
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
#                                         0.4 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-1]) < 2.5:
#                                         # 0.6 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-1]) < 1.67:
#                                         is_goodLine = 1  
                                    
#                                     # 8000中的10-50的2754特殊情况  
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
#                                         (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) > 0 and \
#                                         (data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4]) > 0 and \
#                                         (data[1][i-4] - data[1][i-5])/(data[0][i-4] - data[0][i-5]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
#                                         0.4 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-1]) < 2.5 and \
#                                         (data[1][i] - data[1][i-1]) / (data[1][i-2] - data[1][i-4]) < 0.15:
#                                         ispadd_2754 = True  

                                    

#                                     #俩边差不多长    
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                         (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) > 0 and \
#                                         0.6 < (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-2]) < 1.67:
#                                         is_goodLine = 1 

#                                     #俩边差不多长    
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
#                                         0.6 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-2]) < 1.67:
#                                         is_goodLine = 1
                                    
#                                     # 8000中10-50的2754特殊情况
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
#                                         (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) < 0 and \
#                                         0.6 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-2]) < 1.67 and \
#                                         (data[1][i] - data[1][i+1]) / (data[1][i+1] - data[1][i+2]) < 0.1 and \
#                                         (data[1][i+1] - data[1][i+2]) / (data[1][i+3] - data[1][i+2]) < 0.4:
#                                         is_goodLine = 0
                                    
#                                     #俩边差不多长    
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) > 0 and \
#                                         (data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4]) > 0 and \
#                                         (data[1][i-4] - data[1][i-5])/(data[0][i-4] - data[0][i-5]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
#                                         0.6 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-4]) < 1.67:
#                                         is_goodLine = 1

#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) > 0 and \
#                                         (data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
#                                         0.5 < (data[1][i] - data[1][i+2]) / (data[1][i] - data[1][i-3]) < 1:
#                                         is_goodLine = 1
                                    
#                                     #俩边差不多长    
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) > 0 and \
#                                         (data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) > 0 and \
#                                         0.6 < (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-3]) < 1.67:
#                                         is_goodLine = 1

#                                     #俩边差不多长    
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
#                                         (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
#                                         0.8 < (data[1][i] - data[1][i+3]) / (data[1][i] - data[1][i-2]) < 1.25:
#                                         is_goodLine = 1
#                                         # print('俩边差不uo    350')
                                    
#                                     # 19000的10-50的4310特殊情况    
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
#                                         (data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4]) > 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
#                                         (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
#                                         0.2 < (data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+3]) < 0.3 and \
#                                         0.9 < (data[1][i-3] - data[1][i-2]) / (data[1][i] - data[1][i+3]) < 1.1:
#                                         ispadd_4310 = True
#                                         ispadd_4310_tall = data[1][i] - data[1][i+3]

#                                     #俩边差不多长    
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
#                                         (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
#                                         0.6 < (data[1][i] - data[1][i+3]) / (data[1][i] - data[1][i-1]) < 1.67:
#                                         is_goodLine = 1

#                                     # 19000的10-50的4686的特殊情况
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
#                                         (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) > 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
#                                         (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
#                                         0.6 < (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+3]) < 0.7 and \
#                                         0.8 < (data[1][i] - data[1][i-1]) / (data[1][i-2] - data[1][i-1]) < 0.9 and \
#                                         0.1 < (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1]) < 0.2:
#                                         is_goodLine = 0
                                    
#                                     # 8000的10-50的1037的特殊情况
#                                     # print(center)
#                                     # print((data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1]))
#                                     # print((data[1][i] - data[1][i+3]) / (data[1][i] - data[1][i-1]))
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
#                                         (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
#                                         0.6 < (data[1][i] - data[1][i+3]) / (data[1][i] - data[1][i-1]) < 1.67 and \
#                                         (data[1][i] - data[1][i+1]) / (data[1][i] - data[1][i-1]) < 0.03:
#                                         is_goodLine = 0
                                    
#                                     #俩边差不多长,数据点增加    
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
#                                         (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) < 0 and \
#                                         (data[1][i+5] - data[1][i+4])/(data[0][i+5] - data[0][i+4]) < 0 and \
#                                         (data[1][i+6] - data[1][i+5])/(data[0][i+6] - data[0][i+5]) > 0 and \
#                                         0.8 < (data[1][i] - data[1][i+5]) / (data[1][i] - data[1][i-2]) < 1.25:
#                                         is_goodLine = 1
                                        
#                                     #如果前段太过于短小，那么前段就不能拿出来比较
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
#                                        (data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-2]) < 0.155:
#                                     #    (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 0.155:
#                                         # if 0.5 < (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i+1]) < 1.5:
#                                         if 0.5 < (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i+2]) < 2:
#                                             is_goodLine = 1
                                    

                                    
#                                     #如果前段太过于短小，那么前段就不能拿出来比较，这里增加到了俩组数据
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) > 0 and \
#                                        (data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4]) < 0 and \
#                                        (data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-3]) < 0.155:
#                                     #    (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 0.155:
#                                         # if 0.5 < (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i+1]) < 1.5:
#                                         if 0.5 < (data[1][i] - data[1][i+2]) / (data[1][i-1] - data[1][i-3]) < 2:
#                                             is_goodLine = 1

#                                     #如果前段太过于短小，那么前段就不能拿出来比较，这里增加到了三组数据
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
#                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) > 0 and \
#                                        (data[1][i-3] - data[1][i-4])/(data[0][i-3] - data[0][i-4]) < 0 and \
#                                        (data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-3]) < 0.155:
#                                     #    (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 0.155:
#                                         # if 0.5 < (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i+1]) < 1.5:
#                                         if 0.5 < (data[1][i] - data[1][i+2]) / (data[1][i-1] - data[1][i-3]) < 2:
#                                             is_goodLine = 1

#                                     #如果前前半段过于短小，那么前前半段不能拿出来比较
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
#                                        (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.2:
#                                        #    (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and 
#                                     #    (data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-2]) < 0.2:
#                                     #    (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i+1]) < 0.2:
#                                         if 0.5 < (data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+1]) < 2:
#                                             is_goodLine = 1
                                    
#                                     #如果前前半段过于短小，那么前前半段不能拿出来比较
#                                     if center < data[0][i] < center + 1 and \
#                                        (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) > 0 and \
#                                        (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                        (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) < 0 and \
#                                        (data[1][i+4] - data[1][i+3])/(data[0][i+4] - data[0][i+3]) > 0 and \
#                                        (data[1][i-2] - data[1][i-3])/(data[0][i-2] - data[0][i-3]) < 0 and \
#                                        (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i-1]) < 0.2:
#                                        #    (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and 
#                                     #    (data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-2]) < 0.2:
#                                     #    (data[1][i-1] - data[1][i-2]) / (data[1][i] - data[1][i+1]) < 0.2:
#                                         if 0.5 < (data[1][i] - data[1][i-2]) / (data[1][i] - data[1][i+3]) < 2:
#                                             is_goodLine = 1
                                    
#                                     #后后半段过于短小        
#                                     if center < data[0][i] < center + 1 and \
#                                         (data[1][i-1] - data[1][i-2])/(data[0][i-1] - data[0][i-2]) < 0 and \
#                                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) < 0 and \
#                                         (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and \
#                                         (data[1][i+1] - data[1][i+2]) / (data[1][i] - data[1][i+1]) < 0.2:
#                                         #    (data[1][i+3] - data[1][i+2])/(data[0][i+3] - data[0][i+2]) > 0 and
#                                         #    (data[1][i] - data[1][i-1]) / (data[1][i-1] - data[1][i-2]) < 0.2:
#                                         if 0.5 < (data[1][i] - data[1][i-1]) / (data[1][i] - data[1][i+2]) < 2:
#                                             is_goodLine = 1  

                                  
#                         else:
#                             peak_value.append(data[1][i])
#                     elif before_slope < 0 and slope > 0:
#                         # if center - 2 < data[0][i] < center - 1:
#                         #     isSpecial = True

#                         if center < data[0][i] < center + 1:
#                             isMout = False
#                             break
#                         # if center + 1 < data[0][i] < center + 2:
#                         #     if not isMout_middle:
#                         #         isMout = False
#                         #         break
#                     # elif before_slope < 0 and slope < 0 and abs(before_slope / slope) < 1.2:
#                     #     if center < data[0][i] < center + 1:
#                     #         if not isMout_middle:
#                     #             isMout = False
#                     elif before_slope < 0 and slope < 0:
#                         if center < data[0][i] < center + 1 and (data[1][i-1] - data[1][i+1]) / (data[1][i] - data[1][i+1]) < 0.1 and \
#                         (data[1][i+2] - data[1][i+1])/(data[0][i+2] - data[0][i+1]) > 0:
#                             if not isMout_middle:
#                                 isMout = False
#                     # elif before_slope > 0 and slope > 0 and abs(before_slope / slope) < 1.2:
#                     #     if center < data[0][i] < center + 1:
#                     #         if not isMout_middle:
#                     #             isMout = False
#                         # if center + 1 < data[0][i] < center + 2 and abs(abs(before_slope) - abs(slope)) < 1:
#                         #     isMout = False
#                         #     break

#                 before_slope = slope
#                 #检查是否有峰值，如果没有可以直接退出来
#                 if data[0][i] >= center+2 and not isMout:
#                     break
#         if min_value > value:
#             min_value = value 
#         peak_value.append(value)
#         peak_value = np.array(peak_value)
#         # print('isMout:',isMout)
#         if isMout:
#             trust = (max(mout_value) - min_value) / (max(peak_value) - min_value)
#         if trust < 0.5:
#             is_goodLine = 0
#         if trust > 0.8 and ispadd_2754:
#             is_goodLine = 0
#         # trust += is_goodLine
#         if trust > 0.8 and ispadd_4310:
#             # print(ispadd_4310_tall / (max(peak_value) - min_value))
#             if 0.1 < ispadd_4310_tall / (max(peak_value) - min_value) < 0.2:
#                 is_goodLine = 0
#     return trust,is_goodLine

